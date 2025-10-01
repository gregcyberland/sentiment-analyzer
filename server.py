from fastapi import FastAPI, HTTPException
from models import (
    SentimentAnalysisRequest,
    SentimentAnalysisResponse,
    MessageEnhancementRequest,
    MessageEnhancementResponse
)
from agents.analyzer_agent import analyze_sentiment
from agents.enhancement_agent import enhance_message
from email_service import send_alert_email
import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Sentiment Analysis & Message Enhancement API",
    description="AI-powered sentiment analysis with email alerts and message beautification",
    version="2.0.0"
)

@app.get("/")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "message": "Sentiment Analysis API is running",
        "version": "2.0.0"
    }

@app.post("/analyze", response_model=SentimentAnalysisResponse)
async def analyze_text(request: SentimentAnalysisRequest):
    """
    Analyze text for sentiment, emotions, and potential issues.
    Sends email alerts for concerning content.

    Args:
        request: SentimentAnalysisRequest containing text_to_analyze

    Returns:
        SentimentAnalysisResponse with complete analysis and alert status
    """
    try:
        # Validate input
        if not request.text_to_analyze.strip():
            raise HTTPException(status_code=400, detail="text_to_analyze cannot be empty")

        if len(request.text_to_analyze) > 10000:
            raise HTTPException(status_code=400, detail="Text too long. Maximum 10000 characters allowed.")

        # Analyze sentiment using PydanticAI
        logger.info(f"Analyzing sentiment for text: {request.text_to_analyze[:100]}...")
        result = await analyze_sentiment(request.text_to_analyze)

        # Send email alert if needed
        if result.email_alert_sent:
            logger.info(f"Sending email alert for happiness score: {result.happiness_score}")
            email_sent = send_alert_email(result)

            # Update email_alert_sent status based on actual email sending
            result.email_alert_sent = email_sent

        logger.info(f"Sentiment analysis completed. Alert sent: {result.email_alert_sent}")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during sentiment analysis")

@app.post("/improve", response_model=MessageEnhancementResponse)
async def improve_text(request: MessageEnhancementRequest):
    """
    Improve message with spelling corrections, grammar fixes, and tone beautification.

    Args:
        request: MessageEnhancementRequest containing text_to_improve

    Returns:
        MessageEnhancementResponse with enhanced message and change details
    """
    try:
        # Validate input
        if not request.text_to_improve.strip():
            raise HTTPException(status_code=400, detail="text_to_improve cannot be empty")

        if len(request.text_to_improve) > 5000:
            raise HTTPException(status_code=400, detail="Text too long. Maximum 5000 characters allowed.")

        # Enhance message using PydanticAI
        logger.info(f"Enhancing message: {request.text_to_improve[:100]}...")
        result = await enhance_message(request.text_to_improve)

        logger.info("Message enhancement completed successfully")
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in message enhancement: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during message enhancement")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)