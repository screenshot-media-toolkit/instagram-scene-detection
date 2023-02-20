from typing import List

from google.cloud import vision

from scene_detection.core.settings import settings
from scene_detection.libs.cloud_vision import (
    mean_of_y_coordinate,
    text_of_word,
    words_in_document,
)
from scene_detection.types import DarknetResult, ImageDimension

from .scene_detector import SceneDetector
from .utils import get_position_percentage


class CommentDetector(SceneDetector):
    def detect(
        self,
        objects: List[DarknetResult],
        document: vision.TextAnnotation,
        image_dimension: ImageDimension,
    ) -> float:
        for word in words_in_document(document):
            text = text_of_word(word)

            if "comment" not in text.lower() and "留言" not in text:
                continue

            percentage = get_position_percentage(
                mean_of_y_coordinate(word.bounding_box), image_dimension[1]
            )

            if percentage > settings.detector.comment.acceptable_range:
                continue

            return 1.0

        return 0.0

    @property
    def name(self) -> str:
        return "comment"
