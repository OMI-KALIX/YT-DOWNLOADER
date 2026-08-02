import os
from typing import Dict, Any, Optional
from yt_dlp import YoutubeDL

ALLOWED_HOSTS = {"youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com", "music.youtube.com"}

def is_valid_url(url_str: str) -> bool:
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url_str)
        return parsed.hostname in ALLOWED_HOSTS if parsed.hostname else False
    except Exception:
        return False

def get_yt_dlp_options() -> Dict[str, Any]:
    opts: Dict[str, Any] = {
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        }
    }

    cookie_paths = ["cookies.txt", "/app/cookies.txt", os.environ.get("COOKIES_PATH", "")]
    for path in cookie_paths:
        if path and os.path.exists(path):
            opts["cookiefile"] = path
            break

    return opts

def probe_video(url: str) -> Optional[Dict[str, Any]]:
    options = get_yt_dlp_options()
    
    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return None

            duration = info.get("duration", 0) or 0
            
            # Gather available video heights
            formats = info.get("formats", [])
            heights = set()
            for f in formats:
                h = f.get("height")
                if h and isinstance(h, int):
                    heights.add(h)
            
            qualities = sorted(list(heights), reverse=True)

            return {
                "title": info.get("title") or "Unknown Title",
                "duration": duration,
                "thumbnail": info.get("thumbnail") or info.get("thumbnails", [{}])[-1].get("url", ""),
                "channel": info.get("uploader") or info.get("channel") or "Unknown Creator",
                "qualities": qualities,
                "is_too_long": duration > (30 * 60)
            }
    except Exception as e:
        raise ValueError(f"Failed to probe URL: {str(e)}")
