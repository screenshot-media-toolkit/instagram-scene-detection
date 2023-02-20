from typing import Dict, Iterable

from scene_detection.types import DarknetResult


def label_confidence(objects: Iterable[DarknetResult], labels: Iterable[str]):
    """Get the highest confidence of each label (if present) in the scene."""

    confidences: Dict[str, float] = {}

    for label, conf, _ in objects:
        if label in labels:
            confidences[label] = max(conf, confidences.get(label, 0.0))

    return confidences


def get_position_percentage(pixel: int, image_height: int):
    """Get the percentage of the image height that the pixel is in."""

    return pixel / image_height
