
import json

from intelligence.creative_director import create_creative_briefs


def main():
    print("DIPLOX GEMINI CREATIVE TEST STARTED")

    test_articles = [
        {
            "category": "Technology",
            "title": "The Rise of AI Agents",
            "summary": (
                "AI agents are becoming more capable of "
                "performing multi-step digital tasks."
            ),
            "source": "Diplox Test Data",
            "link": "https://example.com/ai-agents",
            "published": "Test article"
        },
        {
            "category": "Gaming",
            "title": "The Future of Cloud Gaming",
            "summary": (
                "Cloud gaming technology is changing how "
                "players access and experience games."
            ),
            "source": "Diplox Test Data",
            "link": "https://example.com/cloud-gaming",
            "published": "Test article"
        }
    ]

    briefs = create_creative_briefs(
        articles=test_articles,
        count=2
    )

    print("\nCREATIVE DIRECTOR SUCCESS!")
    print(f"Briefs generated: {len(briefs)}")

    print("\nGENERATED CREATIVE BRIEFS:")
    print(json.dumps(
        briefs,
        indent=2,
        ensure_ascii=False
    ))

    print("\nGEMINI CREATIVE TEST COMPLETED SUCCESSFULLY")


if __name__ == "__main__":
    main()
