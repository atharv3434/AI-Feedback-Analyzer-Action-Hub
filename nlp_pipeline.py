import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', quiet=True)

class FeedbackNLP:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.analyzer.lexicon.update({
            'unresponsive': -2.5,
            'overpriced': -2.0,
            'buggy': -2.0,
            'broken': -3.0,
            'superb': 2.5,
            'flawless': 2.5
        })

    def process(self, text: str) -> dict:
        scores = self.analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        is_urgent = scores['neg'] >= 0.35 or compound <= -0.5

        return {
            "sentiment": sentiment,
            "compound_score": round(compound, 3),
            "is_urgent": is_urgent
        }

nlp_engine = FeedbackNLP()