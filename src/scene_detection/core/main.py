import logging
from pathlib import Path
from typing import Any, Dict, List

import click

from scene_detection import detection
from scene_detection.core.settings import settings
from scene_detection.detection import detectors
from scene_detection.detection.scenes import perform_detection
from scene_detection.utils.logger import ColoredLogger

DETECTORS: List[detectors.SceneDetector] = [
    detectors.CommentDetector(),
    detectors.ExternalDetector(),
    detectors.HomepageDetector(),
    detectors.ReelsDetector(),
]

read_input = input


@click.command()
@click.argument("input", type=click.Path(exists=True))
@click.option(
    "-o", "--output", type=click.Path(), default="output.csv", help="Output CSV file"
)
def main(input: str, output: str) -> None:
    """Entry point of the application."""

    logging.setLoggerClass(ColoredLogger)
    logger = logging.getLogger("app")

    settings.ocr.init()

    input_path = Path(input)
    output_path = Path(output)

    if output_path.is_dir():
        new_path = output_path / "output.csv"
        logger.info(
            f"Path {output_path} is a directory, "
            f"result will be stored in to {new_path}."
        )
        output_path = new_path

    if output_path.is_file():
        logger.warning(f"File {output_path} already exists, overwrite? [y/N]")
        answer = read_input()

        if answer.lower() != "y" and answer.lower() != "yes":
            logger.info("Aborting.")
            exit(0)

    if input_path.is_file() and detection.is_image(input_path):
        logger.info(f"Detecting image {input_path}.")
        images = [input_path]
    elif input_path.is_dir():
        logger.info(f"Detecting images in directory {input_path}.")
        images = filter(detection.is_image, input_path.iterdir())
    else:
        logger.error(f"Invalid path {input_path}.")
        exit(1)

    all_rows: List[Dict[str, Any]] = []

    for image in images:
        rows = perform_detection(image, DETECTORS)

        if isinstance(rows, list):
            all_rows.extend(rows)
        else:
            all_rows.append(rows)
