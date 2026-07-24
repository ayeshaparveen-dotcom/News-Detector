import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY", "").strip()

def detect_news(article):
    """Analyze news article for credibility"""
    
    # Demo mode if no valid API key
    if not api_key or api_key == "your_api_key_here":
        return f"""Credibility: Unable to verify (Demo Mode)
Trust Score: N/A
Reason: Please add your OpenAI API key to the .env file to enable real analysis
Summary: This is demo mode. The app is working but needs your OPENAI_API_KEY to analyze news.

To fix:
1. Get your API key from: https://platform.openai.com/api-keys
2. Update .env file with: OPENAI_API_KEY=sk-...
3. Restart the app
"""
    
    # Real API mode with retry logic
    max_retries = 3
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            prompt = f"""
            You are a Fake News Detector.

            Analyze the following news.

            Return in this format only:

            Credibility:
            Trust Score:
            Reason:
            Summary:

            News:
            {article}
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            return response.choices[0].message.content
            
        except Exception as e:
            error_str = str(e)
            
            # Rate limiting error - retry with delay
            if "429" in error_str or "rate_limit" in error_str.lower():
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (attempt + 1)
                    return f"Rate limit reached. Please wait {wait_time} seconds before trying again.\n\nError: {error_str}"
                else:
                    return f"Too many requests. Your API has hit rate limits. Please try again in a few minutes.\n\nError: {error_str}"
            
            # Authentication error
            elif "401" in error_str or "auth" in error_str.lower():
                return f"Authentication Error: Invalid API key. Please check your OPENAI_API_KEY in .env file\n\nError: {error_str}"
            
            # Other errors
            else:
                return f"Error analyzing article: {error_str}"