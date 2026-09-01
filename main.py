from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import engine, get_db
from nlp_pipeline import nlp_engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Feedback Intelligence API")

# Enable CORS for local frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/feedback", response_model=schemas.FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(feedback_in: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    if not feedback_in.text.strip():
        raise HTTPException(status_code=400, detail="Feedback text cannot be empty.")

    nlp_result = nlp_engine.process(feedback_in.text)
    
    db_item = models.Feedback(
        customer_name=feedback_in.customer_name or "Anonymous",
        text=feedback_in.text,
        sentiment=nlp_result["sentiment"],
        compound_score=nlp_result["compound_score"],
        is_urgent=nlp_result["is_urgent"]
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/api/feedback", response_model=List[schemas.FeedbackResponse])
def get_all_feedback(db: Session = Depends(get_db)):
    return db.query(models.Feedback).order_by(models.Feedback.created_at.desc()).all()

@app.get("/api/analytics", response_model=schemas.AnalyticsSummary)
def get_analytics(db: Session = Depends(get_db)):
    feedbacks = db.query(models.Feedback).all()
    total = len(feedbacks)
    urgent = sum(1 for f in feedbacks if f.is_urgent)
    pos = sum(1 for f in feedbacks if f.sentiment == "Positive")
    neg = sum(1 for f in feedbacks if f.sentiment == "Negative")
    neu = sum(1 for f in feedbacks if f.sentiment == "Neutral")

    return schemas.AnalyticsSummary(
        total_feedbacks=total,
        urgent_count=urgent,
        positive_count=pos,
        negative_count=neg,
        neutral_count=neu
    )