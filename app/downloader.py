import os
import tempfile
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

MAX_DURATION_SECONDS = 120 * 60  # 2 hour cap to survive 512MB RAM free tier limits

def run_download(job_id: str, url: str, format_choice: str, quality: str, bitrate: str):
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
    }

    if format_choice == "mp3":
        options["format"] = f"bestaudio[abr<={bitrate}]/bestaudio/best"
        options["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": bitrate,
        }]
    else:
        # For mp4 / video formats
        options["format"] = f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={quality}]+bestaudio/best"
        options["merge_output_format"] = "mp4"

    try:
        # Pre-check info for duration limit
        with YoutubeDL({"noplaylist": True, "quiet": True}) as probe_ydl:
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
        job.status = "error"
        job.error = str(e)
