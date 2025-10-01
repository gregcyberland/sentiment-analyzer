from pydantic_ai import Agent
from models import MessageEnhancementResponse
from pathlib import Path
import os

# Initialize PydanticAI Agent for message enhancement
enhancement_agent = Agent(
    "openai:gpt-4o",
    output_type=MessageEnhancementResponse,
    instructions=Path("enhancement_system_prompt.txt").read_text(encoding="utf-8")
)

async def enhance_message(text: str) -> MessageEnhancementResponse:
    """
    Enhance message with spelling, grammar, and tone improvements using PydanticAI

    Args:
        text: The text to improve

    Returns:
        MessageEnhancementResponse with original text, enhanced version, and changes
    """
    try:
        result = await enhancement_agent.run(
            f"Improve this message by fixing spelling/grammar and beautifying the tone: {text}"
        )
        return result.output

    except Exception as e:
        # Fallback response on error
        return MessageEnhancementResponse(
            original_text=text,
            enhanced_message=text,  # Return original if enhancement fails
            spelling_corrections=[],
            grammar_improvements=["Enhancement service temporarily unavailable"],
            tone_adjustments=[]
        )