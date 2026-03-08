import feedparser
from app.core.config import settings


def fetch_rss(source: str, limit: int = 10):
    feeds = settings.BUSINESS_RSS_FEEDS
    url = feeds.get(source.lower())

    if not url:
        return None

    feed = feedparser.parse(url)

    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "source": source,
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "description": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "image": (
                entry.media_content[0]["url"]
                if hasattr(entry, "media_content") and entry.media_content
                else ""
            )
        })

    return items
