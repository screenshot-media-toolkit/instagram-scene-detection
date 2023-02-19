from bisect import bisect
from functools import partial
from pathlib import Path
from typing import Any, Container, Dict, Iterable, List, Sequence, Union

from google.cloud import vision
from PIL import Image

from scene_detection.core.settings import settings
from scene_detection.detection.detectors import SceneDetector
from scene_detection.libs.cloud_vision import (
    detect_text,
    mean_of_y_coordinate,
    text_in_document,
    text_of_word,
    words_in_document,
)
from scene_detection.libs.detect_objects import detect_objects
from scene_detection.types import DarknetResult, ImageDimension


def get_single_row(
    image_path: Path, context: str, scenes: Union[Container[str], Iterable[str]]
):
    """Represent a single row of the output table."""

    return {
        "user": "test",
        "qid": -1,
        "images": image_path,
        "pid": 0,
        "context": context,
        "percent": 1 - 2 * settings.prediction.invisible_percentage,
        "biggest": 1,
    } | {name: 0 for name in scenes}


def is_image(path: Path):
    """Return whether the input is an image."""

    return path.is_file() and path.suffix in (".png", ".jpg", ".jpeg")


def get_image_dimension(image_path: Path) -> ImageDimension:
    """Return the dimensions of an image."""

    image = Image.open(image_path)
    return image.size


def is_visible(x: int, height: int):
    """Return whether the pixel is in the visible area."""
    return (
        settings.prediction.invisible_percentage
        <= x / height
        <= (1 - settings.prediction.invisible_percentage)
    )


def detect_scenes(image_path: Path, detectors: Sequence[SceneDetector]):
    """Detect the objects and text on the image, return the confidences."""

    objects = detect_objects(image_path)
    document = detect_text(image_path).full_text_annotation
    image_dimension = get_image_dimension(image_path)

    confidences = {
        detector.name: detector.detect(objects, document, image_dimension)
        for detector in detectors
    }

    return objects, document, image_dimension, confidences


def create_row_by_confidence(
    image_path: Path, confidences: Dict[str, float], context: str, scenes: Sequence[str]
):
    """Create a row by confidence of prediction and detection."""

    confident_scene: str = max(confidences, key=confidences.get)

    row = get_single_row(image_path, context, scenes)

    if confidences.get(confident_scene):
        row[confident_scene] = 1
    else:
        row["story"] = 1

    return row


def get_borders(objects: Sequence[DarknetResult], image_height: int):
    """Get all detected borders in the image."""

    borders = (y for label, _, (_, y, *_) in objects if label == "border_options")
    visible = partial(is_visible, height=image_height)
    yield from filter(visible, borders)


def split_text_by_borders(words: Iterable[vision.Word], borders: Iterable[int]):
    """Split the words by the borders."""

    sorted_borders = sorted(borders)
    result: List[List[str]] = [[] for _ in range(len(sorted_borders) + 1)]

    for word in words:
        index = bisect(sorted_borders, mean_of_y_coordinate(word.bounding_box))
        result[index].append(text_of_word(word))

    return result


def get_post_percentages(borders: Iterable[int], image_height: int):
    """Get the percentages of each post takes."""

    invisible_percentage = settings.prediction.invisible_percentage

    borders_in_percentages = [border / image_height for border in borders]

    accumulated_percentage = invisible_percentage
    post_percentages: List[float] = []

    for percentage in borders_in_percentages + [1 - invisible_percentage]:
        percentage_took = percentage - accumulated_percentage
        post_percentages.append(percentage_took)
        accumulated_percentage = percentage

    return post_percentages


def get_splitted_rows(
    row: Dict[str, Any],
    posts_text: Iterable[Iterable[str]],
    posts_percentages: Iterable[float],
):
    """Split the row by the borders."""

    splitted_rows: List[Dict[str, Any]] = []
    max_percentage = max(posts_percentages)

    for post_id, (texts, percentage) in enumerate(zip(posts_text, posts_percentages)):
        row_copy = row.copy()

        row_copy["pid"] = post_id
        row_copy["context"] = " ".join(texts)
        row_copy["percent"] = percentage
        row_copy["biggest"] = 1 if percentage >= max_percentage else 0

        splitted_rows.append(row_copy)

    return splitted_rows


def perform_detection(image_path: Path, detectors: Sequence[SceneDetector]):
    """Perform scene detection on a single image."""

    objects, document, image_dimension, confidences = detect_scenes(
        image_path, detectors
    )

    row = create_row_by_confidence(
        image_path,
        confidences,
        context=" ".join(text_in_document(document)),
        scenes=[*(detector.name for detector in detectors), "story"],
    )

    if not row["homepage"]:
        return row

    borders = list(get_borders(objects, image_dimension[1]))

    posts_text = split_text_by_borders(words_in_document(document), borders)
    posts_percentages = get_post_percentages(borders, image_dimension[1])

    return get_splitted_rows(row, posts_text, posts_percentages)
