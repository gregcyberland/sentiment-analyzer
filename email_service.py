import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
import logging

logger = logging.getLogger(__name__)

def send_alert_email(analysis_result) -> bool:
    """
    Send alert email when concerning content is detected

    Args:
        analysis_result: SentimentAnalysisResponse object with complete analysis

    Returns:
        bool: True if email sent successfully, False otherwise
    """

    # Check if email is configured
    if not config.EMAIL_USER or not config.EMAIL_PASS or not config.ALERT_RECIPIENTS:
        logger.warning("Email credentials or recipients not configured. Skipping email alert.")
        return False

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = config.EMAIL_USER
        msg['To'] = ", ".join(config.ALERT_RECIPIENTS)  # Send to multiple recipients
        msg['Subject'] = "[SYSTEM ALERT] Content Monitoring Notification"

        # Clean Apple-style alert email
        body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 40px 20px;
            background-color: #f5f5f7;
            color: #1d1d1f;
            line-height: 1.47;
            -webkit-text-size-adjust: 100%;
        }}
        .email-container {{
            max-width: 580px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}
        .header {{
            background: #ffffff;
            padding: 40px 40px 20px 40px;
            text-align: center;
            border-bottom: 1px solid #d2d2d7;
        }}
        .title {{
            font-size: 22px;
            font-weight: 600;
            color: #1d1d1f;
            margin: 0 0 8px 0;
            letter-spacing: -0.02em;
        }}
        .subtitle {{
            font-size: 14px;
            color: #86868b;
            margin: 0;
            font-weight: 400;
        }}
        .content {{
            padding: 0 40px 40px 40px;
        }}
        .field {{
            display: flex;
            padding: 16px 0;
            border-bottom: 1px solid #f5f5f7;
            align-items: baseline;
        }}
        .field:last-child {{
            border-bottom: none;
        }}
        .field-name {{
            font-size: 15px;
            font-weight: 400;
            color: #86868b;
            min-width: 140px;
            margin-right: 20px;
        }}
        .field-value {{
            font-size: 15px;
            font-weight: 400;
            color: #1d1d1f;
            flex: 1;
            word-wrap: break-word;
        }}
        .footer {{
            background: #f5f5f7;
            padding: 20px 40px;
            text-align: center;
            border-top: 1px solid #d2d2d7;
        }}
        .footer-text {{
            font-size: 13px;
            color: #86868b;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1 class="title">Content Alert</h1>
            <p class="subtitle">System Notification</p>
        </div>

        <div class="content">
            <div class="field">
                <span class="field-name">Happiness Score:</span>
                <span class="field-value">{analysis_result.happiness_score}</span>
            </div>
            <div class="field">
                <span class="field-name">Overall Tone:</span>
                <span class="field-value">{analysis_result.overall_tone}</span>
            </div>
            <div class="field">
                <span class="field-name">Detected Emotions:</span>
                <span class="field-value">{analysis_result.detected_emotions}</span>
            </div>
            <div class="field">
                <span class="field-name">Situation Summary:</span>
                <span class="field-value">{analysis_result.situation_summary}</span>
            </div>
            <div class="field">
                <span class="field-name">Contains Abuse:</span>
                <span class="field-value">{analysis_result.contains_abuse}</span>
            </div>
            <div class="field">
                <span class="field-name">Happiness Low:</span>
                <span class="field-value">{analysis_result.happiness_low}</span>
            </div>
            <div class="field">
                <span class="field-name">Trigger Message:</span>
                <span class="field-value">{analysis_result.trigger_message}</span>
            </div>
        </div>

        <div class="footer">
            <p class="footer-text">
                {__import__('datetime').datetime.now().strftime('%B %d, %Y at %I:%M %p')} • Content Monitoring System
            </p>
        </div>
    </div>
</body>
</html>"""

        msg.attach(MIMEText(body, 'html'))

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config.EMAIL_USER, config.EMAIL_PASS)

        text = msg.as_string()
        server.sendmail(config.EMAIL_USER, config.ALERT_RECIPIENTS, text)
        server.quit()

        logger.info(f"Alert email sent successfully for happiness score: {analysis_result.happiness_score}")
        return True

    except Exception as e:
        logger.error(f"Failed to send alert email: {e}")
        return False