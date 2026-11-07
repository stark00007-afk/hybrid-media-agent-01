
import json
import os

from google import genai
from config import GEMINI_MODEL


def generate_content(articles):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing.")

    if not articles:
        raise ValueError("No research articles available.")

    client = genai.Client(api_key=api_key)

    research_text = json.dumps(
        articles[:15],
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
You are the creative content engine of HMA-01.

Create exactly TWO original short-form video concepts.

Content categories:
- Technology
- Gaming
- Entrepreneurship

Use the research below:
{research_text}

Requirements:
1. Create engaging, original content.
2. Each video should have a strong opening hook.
3. Write a complete voiceover script.
4. Suggest visual scenes for the editor.
5. Include subtitles for important moments.
6. Create a platform-ready caption.
7. Include relevant hashtags.
8. Suggest an SEO-friendly title.
9. Never invent statistics, quotations or news.
10. Preserve source links for factual claims.
11. Do not copy article text.
12. Use HMA MEDIA as temporary branding.

Return ONLY valid JSON in this format:

{{
  "posts": [
    {{
      "category": "Technology",
      "title": "Video title",
      "hook": "Opening line",
      "script": "Complete voiceover",
      "scenes": [
        "Visual scene 1",
        "Visual scene 2"
      ],
      "subtitles": [
        "Subtitle 1",
        "Subtitle 2"
      ],
      "caption": "Social media caption",
      "hashtags": ["#technology"],
      "sources": ["Original source URL"]
    }}
  ]
}}

Return exactly two posts.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    result = json.loads(response.text)

    posts = result.get("posts", [])

    if len(posts) != 2:
        raise ValueError("Gemini did not generate exactly two posts.")

    return posts


if __name__ == "__main__":
    print("HMA-01 Content Engine is ready.")
    print("It needs research articles and a Gemini API key to generate content.")
