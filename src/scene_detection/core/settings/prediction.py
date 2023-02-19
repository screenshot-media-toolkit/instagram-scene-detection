from pydantic import BaseModel


class PredictionOutputSettings(BaseModel):
    """Parameters related to prediction output."""

    confidence_threshold: float = 0.01
    invisible_percentage: float = 0.13
