
import json
from pathlib import Path

from research_engine import collect_research
from content_engine import generate_content


def main():
    print("HMA-01 starting...")

    # Step 1: Collect research
    articles = collect_research()

    if not articles:
        raise RuntimeError("No research articles found.")

    print(f"Research collected: {len(articles)}")

    # Step 2: Generate two posts using Gemini
    posts = generate_content(articles)

    # Step 3: Save generated posts
    output = {"posts": posts}

    Path("generated_posts.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print("\nCONTENT GENERATION SUCCESSFUL!")

    for number, post in enumerate(posts, start=1):
        print(f"\nPost {number}: {post['title']}")
        print("Category:", post["category"])
        print("Hook:", post["hook"])

    print("\nSaved to generated_posts.json")


if __name__ == "__main__":
    main()
