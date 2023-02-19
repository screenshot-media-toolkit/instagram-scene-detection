from typing import List, Tuple

from google.cloud import vision

from scene_detection.core.settings import settings
from scene_detection.libs.cloud_vision import (
    mean_of_y_coordinate,
    text_of_word,
    words_in_document,
)
from scene_detection.types import DarknetResult

from .scene_detector import SceneDetector
from .utils import get_position_percentage


def is_top_left(x: int, y: int, width: int, height: int):
    return x < width / 2 and y < height / 2


def is_top_right(x: int, y: int, width: int, height: int):
    return x > width / 2 and y < height / 2


def is_bottom_left(x: int, y: int, width: int, height: int):
    return x < width / 2 and y > height / 2


def is_bottom_right(x: int, y: int, width: int, height: int):
    return x > width / 2 and y > height / 2


POSITION_FN = {
    "top-left": is_top_left,
    "top-right": is_top_right,
    "bottom-left": is_bottom_left,
    "bottom-right": is_bottom_right,
}


class ReelsDetector(SceneDetector):
    def detect(
        self,
        objects: List[DarknetResult],
        document: vision.TextAnnotation,
        image_dimension: Tuple[int, int],
    ) -> float:
        confidence = 0.0

        for label, conf, (x, y, *_) in objects:
            label_args = settings.detector.reels.labels.get(label)
            if label_args is None:
                continue

            position_fn = POSITION_FN[label_args.position]
            if not position_fn(x, y, image_dimension[0], image_dimension[1]):
                continue

            confidence += label_args.multiplier * conf

        for word in words_in_document(document):
            text = text_of_word(word)

            if "reels" not in text.lower() and "連續短片" not in text:
                continue

            if (
                get_position_percentage(mean_of_y_coordinate(word.bounding_box))
                > settings.detector.reels.acceptable_range
            ):
                confidence += settings.detector.reels.text_confidence

        return confidence

    @property
    def name(self) -> str:
        return "reels"
