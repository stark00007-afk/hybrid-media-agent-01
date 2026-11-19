 
import json
import os
import re
import time

from google import genai
from google.genai import errors, types

from config import GEMINI_MODEL


# ==============================
# DIPLOX REQUEST CONFIGURATION
# ==============================

REQUEST_TIMEOUT_MS = 90_000
MAX_ATTEMPTS = 2


def clean_json_response(text):
    """Remove Markdown formatting from Gemini JSON output."""

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(r"\s*```$", "", text)

    return text.strip()


def validate_briefs(briefs, expected_count):
    """Validate the creative director's output."""

    if not isinstance(briefs, list):
        raise ValueError("Creative briefs must be a list.")

    if len(briefs) != expected_count:
        raise ValueError(
            f"Expected {expected_count} creative briefs, "
            f"received {len(briefs)}."
        )

    required_fields = [
        "category",
        "concept",
        "storytelling_style",
        "visual_style",
        "hook_direction",
        "narration_style",
        "editing_direction",
        "target_audience",
        "duration_seconds",
        "scenes",
        "creative_notes"
    ]

    for index, brief in enumerate(briefs, start=1):

        if not isinstance(brief, dict):
            raise ValueError(
                f"Brief {index} is not a valid object."
            )

        for field in required_fields:
            if field not in brief:
                raise ValueError(
                    f"Brief {index} is missing: {field}"
                )

        if not isinstance(brief["scenes"], list):
            raise ValueError(
                f"Brief {index} scenes must be a list."
            )

        if not 30 <= brief["duration_seconds"] <= 60:
            raise ValueError(
                f"Brief {index} duration must be "
                "between 30 and 60 seconds."
            )

    return briefs


def create_creative_briefs(articles, count=2):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing."
        )

    if not articles:
        raise ValueError(
            "No research articles available."
        )

    if not isinstance(count, int) or not 1 <= count <= 5:
        raise ValueError(
            "Count must be between 1 and 5."
        )

    # Limit SDK retries so requests cannot silently
    # consume the entire GitHub Actions runtime.
    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=REQUEST_TIMEOUT_MS,
            retry_options=types.HttpRetryOptions(
                attempts=1
            )
        )
    )

    research_data = json.dumps(
        articles[:15],
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
You are the Creative Director of DIPLOX HMA-01.

Your job is to design original, high-quality
short-form video concepts.

You are NOT the scriptwriter.
You are NOT the video editor.

You make creative decisions that other engines
will use to produce the final video.

CONTENT CATEGORIES:
- Technology
- Gaming
- Entrepreneurship

CREATIVE DIRECTION:

Combine these three styles intelligently:

1. Cinematic storytelling
2. Professional documentary
3. Dynamic motion graphics

Do not force all three styles into every video.
Choose the combination that best fits the topic.

YOUR RESPONSIBILITIES:

1. Understand the research.
2. Select interesting and meaningful concepts.
3. Create a distinctive creative direction.
4. Decide the storytelling approach.
5. Define the visual atmosphere.
6. Define the opening hook direction.
7. Decide the narration personality.
8. Suggest professional editing techniques.
9. Plan individual visual scenes.
10. Keep every concept original and informative.

IMPORTANT RULES:

- Never invent facts or statistics.
- Do not present speculation as confirmed news.
- Do not fabricate quotations.
- Do not copy source articles.
- Preserve factual context.
- Avoid repetitive AI-style video concepts.
- Avoid generic introductions.
- Every concept must have a distinct identity.
- Use DIPLOX as the official brand.
- Target short-form videos of 30-60 seconds.
- Make visual directions practical for automated production.

RESEARCH MATERIAL:

{research_data}

RETURN ONLY VALID JSON.

Use exactly this structure:

{{
  "briefs": [
    {{
      "category": "Technology",
      "concept": "Creative video concept",
      "storytelling_style": "Documentary with cinematic elements",
      "visual_style": "Dark cinematic visuals with motion graphics",
      "hook_direction": "How the opening should attract attention",
      "narration_style": "Natural professional narration",
      "editing_direction": "Editing and pacing instructions",
      "target_audience": "Technology enthusiasts",
      "duration_seconds": 45,
      "scenes": [
        {{
          "scene_number": 1,
          "purpose": "Opening",
          "visual_direction": "Scene description",
          "mood": "Curious",
          "duration_seconds": 5
        }}
      ],
      "creative_notes": "Additional creative instructions"
    }}
  ]
}}

Generate exactly {count} different creative briefs.
"""

    for attempt in range(MAX_ATTEMPTS):

        try:
            print(
                f"\nCreative Director: "
                f"attempt {attempt + 1}/{MAX_ATTEMPTS}"
            )

            print(
                f"Request timeout: "
                f"{REQUEST_TIMEOUT_MS // 1000} seconds"
            )

            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            result = json.loads(
                clean_json_response(response.text)
            )

            briefs = result.get("briefs", [])

            validated_briefs = validate_briefs(
                briefs,
                count
            )

            print(
                "Creative Director successfully "
                "generated and validated briefs."
            )

            return validated_briefs

        except errors.ServerError as error:

            is_server_error = (
                getattr(error, "code", None) == 503
                or "503" in str(error)
            )

            if not is_server_error:
                raise

            if attempt == MAX_ATTEMPTS - 1:
                raise RuntimeError(
                    "Gemini server unavailable after "
                    f"{MAX_ATTEMPTS} attempts."
                ) from error

            wait_time = 2

            print(
                f"Gemini server unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

        except Exception as error:

            print(
                "\nCREATIVE DIRECTOR ERROR:"
            )

            print(
                f"{type(error).__name__}: {error}"
            )

            raise RuntimeError(
                "Creative Director request failed. "
                "Check the error above."
            ) from error

    raise RuntimeError(
        "Creative Director failed."
    )


if __name__ == "__main__":
    print("DIPLOX HMA-01 Creative Director")
    print("Module initialized successfully.")
