import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Email Configuration
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ALERT_RECIPIENTS =  ["kristopher.ong@cyberland.edu.sg"]  # Edit this list to change email recipients

# Alert Settings
HAPPINESS_THRESHOLD = 2  # Alert when happiness_score <= 2 (only unhappy, not neutral)

# Validate required environment variables
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

if not EMAIL_USER or not EMAIL_PASS:
    print("Warning: Email credentials not configured. Email alerts will be disabled.")