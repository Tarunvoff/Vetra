"""API Schemas for recommendations and simulations."""

from typing import List, Optional
from pydantic import BaseModel, Field
from kvguard.core.models import Recommendation


class RecommendationListResponse(BaseModel):
    total: int
    recommendations: List[Recommendation]
    gpu_pressure: float
    summary: dict = Field(default_factory=dict)


class SimulateRecommendationRequest(BaseModel):
    gpu_pressure: Optional[float] = Field(default=0.88, ge=0.0, le=1.0)
    num_blocks: Optional[int] = Field(default=10, ge=1, le=100)
