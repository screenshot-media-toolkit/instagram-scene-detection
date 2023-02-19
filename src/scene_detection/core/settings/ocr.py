import os
from pathlib import Path

from pydantic import BaseModel

from .constant import PROJECT_ROOT


class OcrApiSettings(BaseModel):
    """Settings related to Google OCR API."""

    credentials_path: Path = PROJECT_ROOT / "credentials.json"

    def init(self):
        """Inject the credentials path into environment variable."""

        if not self.credentials_path.is_file():
            raise FileNotFoundError(self.credentials_path)

        if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            os.environ.setdefault(
                "GOOGLE_APPLICATION_CREDENTIALS", str(self.credentials_path)
            )
