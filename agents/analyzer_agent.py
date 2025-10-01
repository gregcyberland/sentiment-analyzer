from pydantic_ai import Agent
from models import SentimentAnalysisResponse
from pathlib import Path
import os
import config

# Initialize PydanticAI Agent for sentiment analysis
sentiment_agent = Agent(
    "openai:gpt-4o",
    output_type=SentimentAnalysisResponse,
    instructions=Path("analyzer_system_prompt.txt").read_text(encoding="utf-8").replace('HAPPINESS_THRESHOLD', str(config.HAPPINESS_THRESHOLD))
)

async def analyze_sentiment(text: str) -> SentimentAnalysisResponse:
    """
    Analyze sentiment and detect alerts using PydanticAI

    Args:
        text: The text to analyze (may contain multiple speakers)

    Returns:
        SentimentAnalysisResponse with complete analysis
    """
    try:
        result = await sentiment_agent.run(
            f"Analyze this text for sentiment and potential issues: {text}"
        )
        return result.output

    except Exception as e:
        # Fallback response on error
        return SentimentAnalysisResponse(
            happiness_score=3,
            overall_tone="neutral",
            detected_emotions=["unknown"],
            situation_summary="Processing error occurred.",
            contains_abuse=False,
            happiness_low=False,
            email_alert_sent=False,
            trigger_message=""
        )