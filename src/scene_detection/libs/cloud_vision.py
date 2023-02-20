import statistics
from pathlib import Path

from google.cloud import vision


def detect_text(image_path: Path) -> vision.AnnotateImageResponse:
    """Detect the text in an image (with Google OCR API)."""

    client = vision.ImageAnnotatorClient()

    image = read_file_to_image(image_path)
    feature = vision.Feature(type=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    request = vision.AnnotateImageRequest(image=image, features=[feature])

    return client.annotate_image(request)  # type: ignore


def read_file_to_image(image_path: Path):
    """Read an image from a file and return it as a Google Vision Image."""

    with image_path.open("rb") as image_file:
        content = image_file.read()
        return vision.Image(content=content)


def words_in_document(document: vision.TextAnnotation):
    """Helper function to iterate over words in a document."""

    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                yield from paragraph.words


def text_of_word(word: vision.Word):
    """Helper function to get the text of a word."""

    return "".join(symbol.text for symbol in word.symbols)


def text_in_document(document: vision.TextAnnotation):
    """Helper function to iterate over text in a document."""

    yield from (text_of_word(word) for word in words_in_document(document))


def mean_of_y_coordinate(bounding_box: vision.BoundingPoly) -> int:
    """Helper function to get the mean of the y coordinate of a bounding box."""

    y_coordinates = [vertex.y for vertex in bounding_box.vertices]
    return round(statistics.mean(y_coordinates))
