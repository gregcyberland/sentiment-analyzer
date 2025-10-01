# Sentiment Analyzer for Parent-Teacher Communications

AI-powered sentiment analysis and message enhancement for parent-teacher conversations with email alerts.

## Quick Setup

1. **Create Environment**
```bash
conda create --name sentiment-analyzer python=3.11
conda activate sentiment-analyzer
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and email credentials
```

4. **Configure Settings**
Edit `config.py` to customize:
- `HAPPINESS_THRESHOLD = 2` - Alert threshold (currently ≤2 triggers alerts)
- `ALERT_RECIPIENTS = ["email1", "email2"]` - Who receives alert emails

5. **Run Server**
```bash
python server.py
```
API available at `http://localhost:8000`

## API Endpoints

### Health Check: `GET /`
**Response:**
```json
{
  "status": "healthy",
  "message": "Sentiment Analysis API is running",
  "version": "2.0.0"
}
```

### Analyze Sentiment: `POST /analyze`
**Input:**
```json
{
  "text_to_analyze": "Parent: I'm frustrated with my child's grades. Teacher: Let's discuss this."
}
```
**Output:**
```json
{
  "happiness_score": 2,
  "tone": "frustrated",
  "situation_summary": "A parent is expressing frustration...",
  "contains_abuse": false,
  "happiness_low": true,
  "email_alert_sent": true,
  "trigger_message": "Parent: I'm frustrated with my child's grades"
}
```

### Enhance Message: `POST /improve`
**Input:**
```json
{
  "text_to_improve": "your child is failing everything"
}
```
**Output:**
```json
{
  "original_text": "your child is failing everything",
  "enhanced_message": "I wanted to discuss some academic challenges your child is currently experiencing...",
  "spelling_corrections": [],
  "grammar_improvements": ["Added proper capitalization", "Improved sentence structure"],
  "tone_adjustments": ["Transformed harsh criticism into constructive feedback"]
}
```

## Alert Settings

- **Threshold**: Happiness score ≤ 2 triggers alerts (configure `HAPPINESS_THRESHOLD` in `config.py`)
- **Scale**: 1=Very unhappy, 2=Unhappy (alert), 3=Neutral, 4=Happy, 5=Very happy
- **Triggers**: Low happiness score OR abusive language

## Project Structure

```
├── server.py                          # Main FastAPI application
├── config.py                          # Settings (HAPPINESS_THRESHOLD, ALERT_RECIPIENTS)
├── models.py                          # Pydantic data models
├── email_service.py                   # Email alert functionality
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .env                               # Your environment variables (create from .env.example)
├── analyzer_system_prompt.txt         # AI prompt for sentiment analysis
├── enhancement_system_prompt.txt      # AI prompt for message enhancement
└── agents/
    ├── analyzer_agent.py              # Sentiment analysis agent
    └── enhancement_agent.py           # Message enhancement agent
```

## Configuration Options in config.py

- `HAPPINESS_THRESHOLD` - Set alert threshold (1-5)
- `ALERT_RECIPIENTS` - List of email addresses for alerts
- Environment variables loaded from `.env` file