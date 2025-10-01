from pydantic import BaseModel, Field, model_validator
from typing import List
import config

# INPUT MODELS
class SentimentAnalysisRequest(BaseModel):
    text_to_analyze: str

class MessageEnhancementRequest(BaseModel):
    text_to_improve: str

# OUTPUT MODELS
class SentimentAnalysisResponse(BaseModel):
    happiness_score: int = Field(ge=1, le=5, description="Happiness level from 1-5")
    overall_tone: str
    detected_emotions: List[str]
    situation_summary: str
    contains_abuse: bool
    happiness_low: bool
    email_alert_sent: bool
    trigger_message: str

    @model_validator(mode='after')
    def fix_logic_automatically(self):
        # Automatically calculate correct values regardless of what LLM said
        correct_happiness_low = self.happiness_score <= config.HAPPINESS_THRESHOLD
        correct_alert_sent = self.contains_abuse or correct_happiness_low

        # Override LLM's potentially wrong values with mathematically correct ones
        self.happiness_low = correct_happiness_low
        self.email_alert_sent = correct_alert_sent

        return self

class MessageEnhancementResponse(BaseModel):
    original_text: str
    enhanced_message: str
    spelling_corrections: List[str]
    grammar_improvements: List[str]
    tone_adjustments: List[str]