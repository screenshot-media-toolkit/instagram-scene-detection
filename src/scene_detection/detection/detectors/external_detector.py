from typing import List, Tuple

from google.cloud import vision

from scene_detection.core.settings import settings
from scene_detection.types import DarknetResult

from .scene_detector import SceneDetector
from .utils import label_confidence


class ExternalDetector(SceneDetector):
    def detect(
        self,
        objects: List[DarknetResult],
        document: vision.TextAnnotation,
        image_dimension: Tuple[int, int],
    ) -> float:
        confidences = label_confidence(objects, settings.detector.external.labels)

        return min(
            1.0,
            sum(confidences.values()) / settings.detector.external.confidence_divisor,
        )

    @property
    def name(self) -> str:
        return "external"