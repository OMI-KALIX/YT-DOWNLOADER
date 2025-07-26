# 🎬 YouTube Video Downloader Web App

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-green?logo=flask\&logoColor=white)](https://flask.palletsprojects.com/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-orange)](https://github.com/yt-dlp/yt-dlp)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> A sleek, holographic‑styled web interface to download YouTube videos and audio using Flask & yt-dlp.

---

## 🛠️ Features

* ▶️ **Video & Audio Download**: Download YouTube videos (MP4) or extract audio (MP3).
* ⚙️ **Quality Control**: Choose video resolution (144p–1080p) or audio bitrate (192k–320k).
* 📃 **Playlist & Batch Support**: Easily extendable for playlists (YT-DLP backing).
* 📂 **Custom Output Folder**: All downloads saved under the `downloads/` directory.
* 🔄 **Progress Handling**: Visual progress in terminal; robust error handling.
* 🌐 **Responsive UI**: Futuristic CSS animation & mobile‑friendly design.

---

## 📁 Project Structure

```
video_downloader_flask/
├── app.py               # Flask application logic (download endpoint)
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Main UI template
├── static/
│   ├── style.css        # Holographic styling and animations
└── downloads/           # Auto-created output folder for downloads
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

* Python 3.11+
* `pip`
* `ffmpeg` installed and in your PATH (or update `ffmpeg_location` in `app.py`)

### ⬇️ Installation

1. **Clone the repo**:

   ```bash
   git clone https://github.com/your-username/video_downloader_flask.git
   cd video_downloader_flask
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure `ffmpeg`** is available (or adjust `ffmpeg_location` in `app.py`).

---

## 💻 Running the App

1. **Start the Flask server**:

   ```bash
   python app.py
   ```

2. **Open in browser**:

   Navigate to `http://127.0.0.1:5000/` to access the UI.

3. **Enter a YouTube URL**, select format (MP4 or MP3), choose quality or bitrate, then click **Download**.

---

## 🚩 Configuration Options

| Flag              | Description                                | Default            |
| ----------------- | ------------------------------------------ | ------------------ |
| `--url`           | YouTube video URL                          | (required)         |
| `--format`        | `mp4` or `mp3`                             | `mp4`              |
| `--quality`       | Video height (e.g., `720`, `1080`, `best`) | `best`             |
| `--audio_bitrate` | Audio bitrate in kbps (`192`,`256`,`320`)  | `192` (selectable) |

*Note: These map to form fields in the web UI.*

---

## 🛡️ License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**OMKAR SAWANT**

[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?logo=github)](https://github.com/OMI-KALIX)


Made with ❤️ by OMI-KALIX.

> Feel free to contribute! Pull requests and issues are welcome.
>#This project only for Educational purpose
