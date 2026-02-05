#!/usr/bin/env python3
"""
Video Fetcher for Aerospace Newsletter
Fetches interesting, recent aerospace videos from YouTube
"""

import re
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import urllib.request
import urllib.parse

logger = logging.getLogger(__name__)

# YouTube channels known for quality aerospace content
AEROSPACE_CHANNELS = [
    # Channel name, channel ID
    ("Everyday Astronaut", "UC6uKrU_WqJ1R2HMTY3LIx5Q"),
    ("Scott Manley", "UCxzC4EngIsMrPmbm6Nxvb-A"),
    ("Spaceflight Now", "UCOy2Fq6OTXPhV96e1MNfBfA"),
    ("NASASpaceflight", "UCSUu1lih2RifWkKtDOJdsBA"),
    ("SpaceX", "UCtI0Hodo5o5dUb67FeUjDeA"),
    ("NASA", "UCLA_DiR1FfKNvjuUpBHmylQ"),
    ("Blue Origin", "UCVxTHEKKLxNjGcvVaZindlg"),
    ("The Space Race", "UCHBBSq8Ekmb3XTRDF27z3SA"),
    ("Primal Space", "UClZbmi9JzfnB2CEb0fG8V-g"),
    ("Marcus House", "UCBNHHEoiSF8pcLgqLKVugOw"),
]

# YouTube search queries for aerospace content
SEARCH_QUERIES = [
    "SpaceX launch 2026",
    "NASA Artemis mission",
    "rocket launch",
    "space exploration news",
    "aerospace technology",
    "satellite launch",
    "Boeing Starliner",
    "Blue Origin launch",
    "space station news",
    "rocket engine test",
]


def fetch_featured_video() -> Optional[Dict]:
    """
    Fetch a featured aerospace video from YouTube.
    Returns the most relevant recent video.
    """
    logger.info("🎬 Fetching featured aerospace video...")
    
    videos = []
    
    # Try channel RSS feeds first (most reliable)
    for channel_name, channel_id in AEROSPACE_CHANNELS[:5]:  # Check top 5 channels
        try:
            video = _fetch_from_channel_rss(channel_name, channel_id)
            if video:
                videos.append(video)
                logger.info(f"✅ Found video from {channel_name}: {video['title'][:50]}...")
        except Exception as e:
            logger.debug(f"Could not fetch from {channel_name}: {e}")
    
    # If we got videos, pick the most recent one
    if videos:
        # Sort by published date (most recent first)
        videos.sort(key=lambda x: x.get('published_timestamp', 0), reverse=True)
        best_video = videos[0]
        logger.info(f"🎬 Selected featured video: {best_video['title']}")
        return best_video
    
    # Fallback: try YouTube search
    for query in SEARCH_QUERIES[:3]:
        try:
            video = _fetch_from_youtube_search(query)
            if video:
                logger.info(f"✅ Found video from search: {video['title'][:50]}...")
                return video
        except Exception as e:
            logger.debug(f"Search failed for '{query}': {e}")
    
    logger.warning("⚠️ Could not fetch any featured video")
    return None


def _fetch_from_channel_rss(channel_name: str, channel_id: str) -> Optional[Dict]:
    """Fetch latest video from a YouTube channel's RSS feed"""
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    
    try:
        req = urllib.request.Request(rss_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
        
        # Parse the RSS feed (simple XML parsing)
        # Find the first entry
        entry_match = re.search(r'<entry>(.*?)</entry>', content, re.DOTALL)
        if not entry_match:
            return None
        
        entry = entry_match.group(1)
        
        # Extract video details
        title_match = re.search(r'<title>(.+?)</title>', entry)
        link_match = re.search(r'<link rel="alternate" href="(.+?)"/>', entry)
        video_id_match = re.search(r'<yt:videoId>(.+?)</yt:videoId>', entry)
        published_match = re.search(r'<published>(.+?)</published>', entry)
        thumbnail_match = re.search(r'<media:thumbnail url="(.+?)"', entry)
        description_match = re.search(r'<media:description>(.+?)</media:description>', entry, re.DOTALL)
        
        if not title_match or not video_id_match:
            return None
        
        video_id = video_id_match.group(1)
        title = title_match.group(1)
        
        # Parse published date
        published_timestamp = 0
        published_str = "Recently"
        if published_match:
            try:
                published_dt = datetime.fromisoformat(published_match.group(1).replace('Z', '+00:00'))
                published_timestamp = published_dt.timestamp()
                
                # Check if video is recent (within last 14 days)
                days_ago = (datetime.now(published_dt.tzinfo) - published_dt).days
                if days_ago > 14:
                    return None  # Skip older videos
                
                published_str = published_dt.strftime('%B %d, %Y')
            except:
                pass
        
        video_data = {
            'title': _clean_html(title),
            'video_id': video_id,
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'thumbnail': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
            'thumbnail_hq': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            'channel': channel_name,
            'published': published_str,
            'published_timestamp': published_timestamp,
            'description': _clean_html(description_match.group(1)[:300] if description_match else ""),
            'embed_url': f"https://www.youtube.com/embed/{video_id}",
        }
        
        return video_data
        
    except Exception as e:
        logger.debug(f"RSS fetch error for {channel_name}: {e}")
        return None


def _fetch_from_youtube_search(query: str) -> Optional[Dict]:
    """Fallback: Fetch video by searching YouTube (basic scraping)"""
    try:
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}&sp=CAI"  # Sort by upload date
        
        req = urllib.request.Request(search_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
        
        # Find video IDs in the page
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', content)
        titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}', content)
        
        if video_ids and titles:
            video_id = video_ids[0]
            title = titles[0]
            
            return {
                'title': _clean_html(title),
                'video_id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'thumbnail': f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
                'thumbnail_hq': f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                'channel': "YouTube Search",
                'published': "Recent",
                'published_timestamp': 0,
                'description': f"Found via search: {query}",
                'embed_url': f"https://www.youtube.com/embed/{video_id}",
            }
        
        return None
        
    except Exception as e:
        logger.debug(f"Search error for '{query}': {e}")
        return None


def _clean_html(text: str) -> str:
    """Remove HTML entities and tags from text"""
    # Decode common HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&apos;', "'")
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


def format_video_for_email_html(video: Dict) -> str:
    """Generate HTML snippet for embedding video in newsletter email"""
    if not video:
        return ""
    
    return f"""
    <div class="featured-video" style="margin: 30px 0; padding: 25px; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); border-radius: 12px; text-align: center;">
        <h2 style="color: #e94560; font-size: 1.5rem; margin-bottom: 20px; font-weight: 600;">
            🎬 Featured Video of the Week
        </h2>
        <a href="{video['url']}" target="_blank" style="display: block; text-decoration: none;">
            <div style="position: relative; display: inline-block; max-width: 100%;">
                <img src="{video['thumbnail_hq']}" 
                     alt="{video['title']}" 
                     style="max-width: 100%; width: 560px; border-radius: 8px; box-shadow: 0 8px 25px rgba(0,0,0,0.4);"
                     onerror="this.src='{video['thumbnail']}'"
                />
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 70px; height: 70px; background: rgba(229, 69, 96, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                    <div style="width: 0; height: 0; border-left: 24px solid white; border-top: 14px solid transparent; border-bottom: 14px solid transparent; margin-left: 6px;"></div>
                </div>
            </div>
        </a>
        <div style="margin-top: 20px;">
            <h3 style="color: white; font-size: 1.2rem; margin-bottom: 10px; line-height: 1.4;">
                <a href="{video['url']}" target="_blank" style="color: white; text-decoration: none;">
                    {video['title']}
                </a>
            </h3>
            <p style="color: #a0aec0; font-size: 0.9rem; margin-bottom: 15px;">
                📺 {video['channel']} • 📅 {video['published']}
            </p>
            <a href="{video['url']}" target="_blank" 
               style="display: inline-block; background: linear-gradient(135deg, #e94560 0%, #f5576c 100%); color: white; padding: 12px 30px; border-radius: 25px; text-decoration: none; font-weight: 600; font-size: 0.95rem; box-shadow: 0 4px 15px rgba(233, 69, 96, 0.4);">
                ▶ Watch on YouTube
            </a>
        </div>
    </div>
    """


def format_video_for_email_text(video: Dict) -> str:
    """Generate plain text snippet for video in newsletter email"""
    if not video:
        return ""
    
    return f"""
🎬 FEATURED VIDEO OF THE WEEK
{'=' * 40}

{video['title']}
📺 Channel: {video['channel']}
📅 Published: {video['published']}

▶ Watch here: {video['url']}

"""


if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    print("🧪 Testing video fetcher...")
    
    video = fetch_featured_video()
    
    if video:
        print("\n✅ Successfully fetched video:")
        print(f"   Title: {video['title']}")
        print(f"   Channel: {video['channel']}")
        print(f"   URL: {video['url']}")
        print(f"   Published: {video['published']}")
        print(f"\n📧 Email HTML preview:")
        print(format_video_for_email_html(video)[:500] + "...")
    else:
        print("❌ Could not fetch any video")
