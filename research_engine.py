
import feedparser
from urllib.parse import quote
from datetime import datetime, timezone

# HMA-01 Autonomous Research Engine

CATEGORIES = {
    "Technology": "latest technology AI innovations",
    "Gaming": "latest gaming industry news",
    "Entrepreneurship": "startups business entrepreneurship"
}


def search_news(category, query, limit=5):
    search_url = (
        "https://news.google.com/rss/search?q="
        + quote(query)
        + "&hl=en-IN&gl=IN&ceid=IN:en"
    )

    feed = feedparser.parse(search_url)
    results = []

    for entry in feed.entries[:limit]:
        results.append({
            "category": category,
            "title": entry.get("title", "Untitled"),
            "summary": entry.get("summary", ""),
            "source": entry.get("source", {}).get("title", "Unknown"),
            "link": entry.get("link", ""),
            "published": entry.get("published", "")
        })

    return results


def collect_research():
    research = []

    for category, query in CATEGORIES.items():
        try:
            articles = search_news(category, query)
            research.extend(articles)
            print(f"{category}: found {len(articles)} articles")

        except Exception as error:
            print(f"{category} research failed: {error}")

    return research


if __name__ == "__main__":
    print("HMA-01 Research Engine starting...")
    articles = collect_research()

    print(f"\nTotal articles collected: {len(articles)}")

    for article in articles:
        print("\nCategory:", article["category"])
        print("Headline:", article["title"])
        print("Source:", article["source"])
        print("Link:", article["link"])

    print("\nResearch completed.")
