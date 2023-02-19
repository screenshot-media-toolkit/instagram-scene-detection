import tomlkit
from pydantic import BaseModel

from .constant import PROJECT_ROOT
from .detector import DetectorSettings
from .model import ModelConfigurationSettings
from .ocr import OcrApiSettings
from .prediction import PredictionOutputSettings


class ApplicationSettings(BaseModel):
    """All settings related to the application."""

    prediction = PredictionOutputSettings()
    model = ModelConfigurationSettings()
    ocr = OcrApiSettings()
    detector = DetectorSettings()


settings_toml = PROJECT_ROOT / "settings.toml"
toml_data = tomlkit.parse(settings_toml.read_text())
settings = ApplicationSettings(**toml_data)
