def detect_news(article):
    article = article.lower()
    fake_words = [
    "shocking",
     "miracle",
     "breaking",
     "click here",
     "100% true",
     "secret",
     "viral"
     ]

    score = 0
    for word in fake_words:
         if word in article:
            score += 1
    if score >= 2:
        return """Credibility: Fake News ❌
Trust Score: 25%
Reason:
The article contains suspicious or clickbait words.
Summary:
 This news is likely fake.
"""
    else:
       return """Credibility: Real News ✅

 Trust Score: 85%
 Reason:
 No suspicious keywords were found.
 Summary:
This news appears to be genuine.
 """