from fastapi import APIRouter, HTTPException
import feedparser
from typing import List, Dict
from app.core.config import settings

router = APIRouter()

@router.get("/")
def list_sources():
    """List available RSS sources"""
    return {
        "sources": list(settings.BUSINESS_RSS_FEEDS.keys()),
        "count": len(settings.BUSINESS_RSS_FEEDS)
    }

@router.get("/{source}")
def get_rss_feed(source: str, limit: int = 20):
    """Get RSS feed for specific source"""
    if source not in settings.BUSINESS_RSS_FEEDS:
        raise HTTPException(status_code=404, detail="Invalid RSS source")
    
    url = settings.BUSINESS_RSS_FEEDS[source]
    feed = feedparser.parse(url)
    
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "title": entry.get("title"),
            "link": entry.get("link"),
            "published": entry.get("published"),
            "summary": entry.get("summary", entry.get("description", "")),
            "author": entry.get("author", ""),
            "guid": entry.get("id", "")
        })
    
    return {
        "source": source,
        "title": feed.feed.get("title", ""),
        "link": feed.feed.get("link", ""),
        "description": feed.feed.get("description", ""),
        "items": items,
        "count": len(items)
    }

@router.get("/all/latest")
def get_all_latest(limit: int = 10):
    """Get latest items from all RSS feeds"""
    all_items = []
    
    for source, url in settings.BUSINESS_RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:  # Get 5 from each
            all_items.append({
                "source": source,
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": entry.get("published"),
                "summary": entry.get("summary", "")
            })
    
    # Sort by published date (newest first)
    all_items.sort(key=lambda x: x.get("published", ""), reverse=True)
    
    return {
        "items": all_items[:limit],
        "total_sources": len(settings.BUSINESS_RSS_FEEDS)
    }