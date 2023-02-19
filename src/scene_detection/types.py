from typing import Tuple


class ImageDimension(Tuple[int, int]):
    """Represents the dimensions of an image (width, height)."""


class BoxDimension(Tuple[int, int, int, int]):
    """Represents the bounding box of an object (x, y, width, height)."""


class DarknetResult(Tuple[str, float, BoxDimension]):
    """The detection output of darknet (label, confidence, bounding box)."""
