from datetime import datetime
from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    customer_name: str = "Anonymous"
    text: str

class FeedbackResponse(BaseModel):
    id: int
    customer_name: str
    text: str
    sentiment: str
    compound_score: float
    is_urgent: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AnalyticsSummary(BaseModel):
    total_feedbacks: int
    urgent_count: int
    positive_count: int
    negative_count: int
    neutral_count: int