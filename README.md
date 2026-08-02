# 🎬 Media Service — FastAPI + ffmpeg (Render Free Tier)

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC?logo=tailwindcss)](https://tailwindcss.com/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-orange)](https://github.com/yt-dlp/yt-dlp)
[![Render](https://img.shields.io/badge/Render-Free%20Tier-46E3B7?logo=render)](https://render.com/)

> Lightweight, high-performance media downloader built with FastAPI, Vite + React, and ffmpeg. Specifically engineered to survive Render's free tier constraints (512MB RAM, ephemeral filesystem, spin-down idle limits).

---

## 🛠️ Architecture & Constraints

```
┌─────────────────────────────────────────────┐
│              Render Web Service               │
│  ┌───────────────────────────────────────┐   │
│  │   FastAPI app (uvicorn)                │   │
│  │   - serves API (/api/*)                │   │
│  │   - serves built frontend (static/)    │   │
│  │   - in-memory job dictionary           │   │
│  │   - BackgroundTasks (yt-dlp + ffmpeg)  │   │
│  └───────────────────────────────────────┘   │
│  ffmpeg installed at OS level in Docker image│
│  /tmp used for ephemeral download storage     │
└─────────────────────────────────────────────┘
```

- **512MB RAM Friendly**: In-memory job state without Redis, Celery, or ORM overhead.
- **Ephemeral Storage**: Files are saved temporarily and automatically deleted immediately after being streamed to the user.
- **Duration Protection**: Videos exceeding 30 minutes are automatically guarded to prevent RAM/CPU exhaust.
- **Single Container**: Multi-stage Docker build compiles the TSX frontend and packages it with Python + ffmpeg into a single image.

---

## 📁 Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI application & route endpoints
│   ├── jobs.py          # In-memory job state dataclass & dictionary
│   ├── downloader.py    # yt-dlp + ffmpeg download & post-processing worker
│   └── probe.py         # Metadata probing & host allowlist validation
├── frontend/            # Vite + React + TypeScript + Tailwind CSS UI
│   ├── src/
│   │   ├── App.tsx      # Dark dashboard UI & polling logic
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── Dockerfile           # Multi-stage Docker build (Node -> Python + ffmpeg)
├── render.yaml          # Render service deployment blueprint
├── requirements.txt     # Backend dependencies
└── README.md
```

---

## 💻 Local Development

### 1. Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI Uvicorn dev server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## 🚀 Deploying to Render

1. Push your repository to GitHub.
2. Log into [Render Dashboard](https://dashboard.render.com/) and click **New +** -> **Blueprint**.
3. Connect your repository (`render.yaml` will be auto-detected).
4. Click **Apply**.

Render will build the Docker container and deploy the service on the free tier.

---

## 🛠️ Troubleshooting & Anti-Bot Setup

For detailed step-by-step instructions on resolving YouTube bot verification (`Sign in to confirm you're not a bot`) and Render read-only cookie mount issues (`[Errno 30]`), see **[TROUBLESHOOTING.md](file:///c:/Users/omusa/Downloads/YT-DOWNLOADER/TROUBLESHOOTING.md)**.

---

## 🛡️ License & Educational Notice

Distributed under the **MIT License**.

> **Educational Purpose Only**: This tool is designed strictly for educational purposes. Please respect copyright laws and content creators' rights.

Made with ❤️ by OMI-KALIX.
