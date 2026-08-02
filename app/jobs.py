from typing import Dict, Optional
from dataclasses import dataclass
import uuid

@dataclass
class Job:
    id: str
    status: str = "queued"     # queued | downloading | converting | done | error
    progress: float = 0.0
    filepath: Optional[str] = None
    error: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[int] = None
    format: Optional[str] = None
    quality: Optional[str] = None

JOBS: Dict[str, Job] = {}   # Process-local in-memory job store for single Render free tier instance

def new_job(title: Optional[str] = None, duration: Optional[int] = None, format_choice: Optional[str] = None, quality: Optional[str] = None) -> Job:
    job = Job(
        id=str(uuid.uuid4()),
        title=title,
        duration=duration,
        format=format_choice,
        quality=quality
    )
    JOBS[job.id] = job
    return job

def get_job(job_id: str) -> Optional[Job]:
    return JOBS.get(job_id)
