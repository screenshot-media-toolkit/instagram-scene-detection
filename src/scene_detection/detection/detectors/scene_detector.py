from abc import ABC, abstractmethod
from typing import List

from google.cloud import vision

from scene_detection.types import DarknetResult, ImageDimension


class SceneDetector(ABC):
    """Interface for scene detectors."""

    @abstractmethod
    def detect(
        self,
        objects: List[DarknetResult],
        document: vision.TextAnnotation,
        image_dimension: ImageDimension,
    ) -> float:
        """Compute the scene detection confidence score for the given objects."""

        raise NotImplementedError()

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the scene detector."""

        raise NotImplementedError()
