import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List

try:
    from .jobs import JOBS, new_job, get_job
    from .downloader import run_download
    from .probe import probe_video, ALLOWED_HOSTS
except ImportError:
    from jobs import JOBS, new_job, get_job
    from downloader import run_download
    from probe import probe_video, ALLOWED_HOSTS

app = FastAPI(title="Media Downloader API", version="1.0.0")

@app.on_event("startup")
def startup_cookies_log():
    cookies_env = os.environ.get("COOKIES_FILE", "")
    candidates = [
        cookies_env,
        os.environ.get("COOKIES_PATH", ""),
        "/etc/secrets/youtube_cookies.txt",
        "youtube_cookies.txt",
        "cookies.txt",
        "/app/cookies.txt"
    ]
    found = next((p for p in candidates if p and os.path.exists(p)), None)
    print(f"[startup] COOKIES_FILE env='{cookies_env}', active_file='{found}', exists={bool(found)}")

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProbeRequest(BaseModel):
    url: HttpUrl

class DownloadRequest(BaseModel):
    url: HttpUrl
    format: str = "mp4"       # mp4 | mp3
    quality: str = "720"      # 1080 | 720 | 480 | 360
    bitrate: str = "192"      # 320 | 256 | 192 | 128

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/api/probe")
def probe_endpoint(req: ProbeRequest):
    host = req.url.host or ""
    if host.lower() not in ALLOWED_HOSTS:
        raise HTTPException(status_code=400, detail="Only YouTube URLs are supported")
    try:
        data = probe_video(str(req.url))
        if not data:
            raise HTTPException(status_code=404, detail="Could not extract video metadata")
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/jobs")
def create_job(req: DownloadRequest, bg: BackgroundTasks):
    host = req.url.host or ""
    if host.lower() not in ALLOWED_HOSTS:
        raise HTTPException(status_code=400, detail="Only YouTube URLs are supported (youtube.com, youtu.be)")

    job = new_job(format_choice=req.format, quality=req.quality)
    bg.add_task(run_download, job.id, str(req.url), req.format, req.quality, req.bitrate)
    return {"job_id": job.id}

@app.get("/api/jobs/{job_id}")
def job_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": job.id,
        "status": job.status,
        "progress": job.progress,
        "error": job.error,
        "title": job.title,
        "duration": job.duration,
        "format": job.format,
        "quality": job.quality,
        "has_file": bool(job.filepath and os.path.exists(job.filepath))
    }

@app.get("/api/jobs/{job_id}/file")
def get_file(job_id: str, bg: BackgroundTasks):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "done" or not job.filepath or not os.path.exists(job.filepath):
        raise HTTPException(status_code=404, detail="File not ready or unavailable")

    filepath = job.filepath
    filename = os.path.basename(filepath)

    def cleanup():
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass
        JOBS.pop(job_id, None)

    bg.add_task(cleanup)
    return FileResponse(path=filepath, filename=filename, media_type="application/octet-stream")

# Mount static files directory if present (serves built React frontend)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if not os.path.exists(static_dir):
    static_dir = "static"

if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
