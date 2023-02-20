from pathlib import Path
from typing import List

from scene_detection.core.settings import settings
from scene_detection.types import DarknetResult

from .darknet import performDetect  # type: ignore


def detect_objects(image_path: Path) -> List[DarknetResult]:
    """Detect objects in the image."""

    return performDetect(  # type: ignore
        imagePath=str(image_path),
        thresh=settings.prediction.confidence_threshold,
        configPath=str(settings.model.config_path),
        weightPath=str(settings.model.weights_path),
        metaPath=str(settings.model.metadata_path),
        showImage=False,
    )
