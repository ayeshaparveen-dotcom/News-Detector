import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env
load_dotenv(dotenv_path=".env")

# Get Groq API key
API_KEY = os.getenv("GROQ_API_KEY", "").strip()

# Check whether the key was loaded
print("GROQ KEY LOADED:", bool(API_KEY))

# Connect to Groq using the OpenAI-compatible API
if API_KEY:
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
else:
    client = None


def detect_news(article):
    """Analyze a news article using Groq."""

    if not article or not article.strip():
        return "Please enter a news article to analyze."

    if client is None:
        return """Credibility: Unable to analyze
Trust Score: N/A
Reason: GROQ_API_KEY is not configured.
Summary: Add your Groq API key to the .env file and restart the application.
Fact Check Needed: Yes
"""

    prompt = f"""
You are an AI news-analysis assistant.

Analyze the following news article carefully.

Important:
- Do not claim that the article is definitely true or definitely false
  based only on the article text.
- Distinguish between factual claims, opinions, and unsupported claims.
- Give a credibility assessment based only on the provided article.
- External fact-checking is required for final verification.

Return exactly this format:

Credibility: [High / Medium / Low / Unable to determine]
Trust Score: [0-100]
Reason: [short explanation]
Summary: [2-3 sentence summary]
Fact Check Needed: [Yes]

Article:
{article}
"""

    try:
        response = client.responses.create(
            model="openai/gpt-oss-20b",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"""Error analyzing article.

Please check your Groq API key, internet connection,
and model access.

Error: {str(e)}
"""