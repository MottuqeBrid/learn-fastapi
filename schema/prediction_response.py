from pydantic import BaseModel, Field
from typing import Dict


class PredictionResponse(BaseModel):
    prediction_category: str = Field(
        ...,
        description="The   predicted insurance premium category",
        title="Prediction Category",
        example="High",
    )
    confidence: float = Field(
        ...,
        description="Model's confidence score for the predicted class (range: 0 to 1)",
        title="Confidence Score",
        example=0.8,
    )
    class_probabilities: Dict[str, float] = Field(
        ...,
        description="Probabilityy distribution across all classes",
        title="Class Probabilities",
        example={"Low": 0.01, "Medium": 0.15, "High": 0.84},
    )
