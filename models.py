from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, default="Anonymous")
    text = Column(String, nullable=False)
    sentiment = Column(String, nullable=False)
    compound_score = Column(Float, nullable=False)
    is_urgent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)