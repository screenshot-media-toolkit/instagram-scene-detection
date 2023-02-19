from typing import Container, Dict, Iterable, List, Union

from .scene_detector import DetectionResult


def label_confidence(
    objects: List[DetectionResult], labels: Union[Container[str], Iterable[str]]
):
    """Get the highest confidence of each label (if present) in the scene."""

    confidences: Dict[str, float] = {}

    for label, conf, _ in objects:
        if label in labels:
            confidences[label] = max(conf, confidences.get(label, 0.0))

    return confidences


def get_position_percentage(pixel: int, image_height: int):
    """Get the percentage of the image height that the pixel is in."""

    return pixel / image_height
