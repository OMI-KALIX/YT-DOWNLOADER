import os
import tempfile
import time
from typing import Dict, Any
from yt_dlp import YoutubeDL
try:
    from .jobs import JOBS
except ImportError:
    from jobs import JOBS

# Use system temp directory or /tmp/downloads (ephemeral storage)
SYSTEM_TEMP = tempfile.gettempdir()
DOWNLOAD_DIR = os.path.join(SYSTEM_TEMP, "yt_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

MAX_DURATION_SECONDS = 30 * 60  # 30 minute cap to survive 512MB RAM free tier limits

def friendly_error(msg: str) -> str:
    if "Sign in to confirm" in msg or "not a bot" in msg or "BotGuard" in msg:
        return "YouTube anti-bot verification triggered. Please try again in a few moments or ensure cookies.txt is updated."
    if "Video unavailable" in msg:
        return "This video is unavailable or private."
    return msg

def run_download(job_id: str, url: str, format_choice: str, quality: str, bitrate: str, _retry: bool = False):
    job = JOBS.get(job_id)
    if not job:
        return

    job.status = "downloading"
    job.progress = 0.0

    def hook(d: Dict[str, Any]):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total and total > 0:
                job.progress = round(min(100.0, max(0.0, (downloaded / total) * 100)), 1)
        elif d["status"] == "finished":
            job.status = "converting"
            job.progress = 99.0

    outtmpl_pattern = os.path.join(DOWNLOAD_DIR, f"{job_id}.%(ext)s")

    options: Dict[str, Any] = {
        "outtmpl": outtmpl_pattern,
        "progress_hooks": [hook],
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"]
            }
        }
    }

    # Support COOKIES_FILE env var, Render Secret Files (/etc/secrets/youtube_cookies.txt), or local files
    cookie_paths = [
        os.environ.get("COOKIES_FILE", ""),
        os.environ.get("COOKIES_PATH", ""),
        "/etc/secrets/youtube_cookies.txt",
        "youtube_cookies.txt",
        "cookies.txt",
        "/app/cookies.txt"
    ]
    for path in cookie_paths:
        if path and os.path.exists(path):
            options["cookiefile"] = path
            print(f"[yt-dlp download] Using cookiefile: {path}")
            break

    proxy = os.environ.get("PROXY_URL")
    if proxy:
        options["proxy"] = proxy

    ffmpeg_loc = os.environ.get("FFMPEG_LOCATION")
    if ffmpeg_loc:
        options["ffmpeg_location"] = ffmpeg_loc

    # FFmpeg Optimization: cap threads to 2 (prevents RAM/CPU exhaustion) & add +faststart for instant progressive web playback
    options["postprocessor_args"] = {
        "ffmpeg": ["-threads", "2", "-movflags", "+faststart"]
    }

    if format_choice == "mp3":
        options["format"] = f"bestaudio[abr<={bitrate}]/bestaudio/best"
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": bitrate,
        }]
    else:
        # High resolution format selection (4K/2K/1080p/720p) merged into MP4 container
        if quality == "best" or quality == "2160":
            options["format"] = "bestvideo+bestaudio/best"
        else:
            options["format"] = f"bestvideo[height<={quality}]+bestaudio/best"
        options["merge_output_format"] = "mp4"

    probe_opts = {k: v for k, v in options.items() if k not in ("progress_hooks", "outtmpl", "format", "postprocessors", "merge_output_format", "postprocessor_args")}

    try:
        # Pre-check info for duration limit
        with YoutubeDL(probe_opts) as probe_ydl:
            info_meta = probe_ydl.extract_info(url, download=False)
            if info_meta:
                duration = info_meta.get("duration", 0) or 0
                job.title = info_meta.get("title") or "video"
                job.duration = duration
                if duration > MAX_DURATION_SECONDS:
                    job.status = "error"
                    job.error = "Video duration exceeds maximum 30 minute limit for free tier."
                    return

        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if format_choice == "mp3":
                base, _ = os.path.splitext(filename)
                filename = base + ".mp3"
            elif not os.path.exists(filename):
                # If merged into mp4
                base, _ = os.path.splitext(filename)
                if os.path.exists(base + ".mp4"):
                    filename = base + ".mp4"

            if os.path.exists(filename):
                job.filepath = filename
                job.status = "done"
                job.progress = 100.0
            else:
                # Search directory for file matching job_id
                matched = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if f.startswith(job_id)]
                if matched:
                    job.filepath = matched[0]
                    job.status = "done"
                    job.progress = 100.0
                else:
                    job.status = "error"
                    job.error = "Output file not found after processing."

    except Exception as e:
        msg = str(e)
        if ("Sign in to confirm" in msg or "not a bot" in msg or "BotGuard" in msg) and not _retry:
            time.sleep(3)
            return run_download(job_id, url, format_choice, quality, bitrate, _retry=True)
        job.status = "error"
        job.error = friendly_error(msg)
