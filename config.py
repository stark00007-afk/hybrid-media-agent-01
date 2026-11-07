import os
from zoneinfo import ZoneInfo

# HMA-01 basic settings

PROJECT_NAME = "HMA-01"
BRAND_NAME = "DIPLOX"

# AI configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Discord configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Publishing configuration
TIMEZONE = ZoneInfo("Asia/Kolkata")

PUBLISH_TIMES = ["09:00", "18:00"]
PREVIEW_TIMES = ["08:30", "17:30"]

CANCELLATION_WINDOW_MINUTES = 30

# Content categories
CONTENT_CATEGORIES = [
    "Technology",
    "Gaming",
    "Entrepreneurship"
]

# Safety settings
PUBLISH_ONLY_IF_APPROVED = True
FAIL_CLOSED = True
