from pathlib import Path

from pydantic import BaseModel

from .constant import PROJECT_ROOT


class ModelConfigurationSettings(BaseModel):
    """Parameters related to prediction model configuration."""

    metadata_path: Path = PROJECT_ROOT / "yolov3.data"
    config_path: Path = PROJECT_ROOT / "yolov3.cfg"
    weights_path: Path = PROJECT_ROOT / "yolov3.weights"
