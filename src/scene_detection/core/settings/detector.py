from typing import Dict, Literal, Tuple

from pydantic import BaseModel


class CommentDetectorSettings(BaseModel):
    """Paramters for comment detectors."""

    acceptable_range: float = 0.15


class HomepageDetectorSettings(BaseModel):
    """Paramters for homepage detectors."""

    confidence_divisor: float = 3
    labels: Tuple[str] = ("ins_logo", "icon_nav", "icon_msg", "icon_bookmark")


class ExternalDetectorSettings(BaseModel):
    """Paramters for external link detectors."""

    confidence_divisor: float = 2
    labels: Tuple[str] = ("external_close", "external_info")


class ReelsLabel(BaseModel):
    """Position and confidence multiplier for a reels label."""

    multiplier: float
    position: Literal["top-left", "top-right", "bottom-left", "bottom-right"]


class ReelsDetectorSettings(BaseModel):
    """Paramters for reels detectors."""

    text_confidence: float = 0.15
    acceptable_range: float = 0.2
    labels: Dict[str, ReelsLabel] = {
        "reels_action": ReelsLabel(multiplier=0.7, position="bottom-right"),
        "reels_camera": ReelsLabel(multiplier=0.15, position="top-right"),
    }


class DetectorSettings(BaseModel):
    """Parameters for detectors."""

    comment = CommentDetectorSettings()
    homepage = HomepageDetectorSettings()
    external = ExternalDetectorSettings()
    reels = ReelsDetectorSettings()
