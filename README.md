# 📹 Video Downloader

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![Pytube](https://img.shields.io/badge/Pytube-10.9.3-orange?logo=python\&logoColor=white)](https://github.com/pytube/pytube)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> A simple, command-line video downloader supporting YouTube and other platforms, with resolution control, playlist support, and audio extraction.

---

## 📌 Features

* 🎥 **Download Videos** by URL
* ⚙️ **Quality Selection**: pick resolution (1080p, 720p, etc.)
* 📜 **Playlist Support**: download entire playlists in batch
* 🎵 **Audio Extraction**: extract audio as MP3
* 📂 **Custom Output Directory**
* 🔄 **Progress Display**
* 🧰 **Cross-Platform**: works on Windows, macOS & Linux

---

## ⚙️ Project Structure

```
video_downloader/
├── downloader.py      # Main script
├── requirements.txt   # Python dependencies
├── LICENSE            # MIT License
└── README.md          # This file
```

---

## 🚀 Getting Started

### 🔧 Requirements

* Python 3.11 or higher
* `pip` package manager
* Internet connection

### ⚙️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/video_downloader.git
   cd video_downloader
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

All commands are run from the project root directory.

1. **Download a single video**:

   ```bash
   python app.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
   ```

2. **Specify resolution** (e.g., 720p):

   ```bash
   python app.py --url "https://youtu.be/VIDEO_ID" --quality 720p
   ```

3. **Download a playlist**:

   ```bash
   python app.py --playlist "https://www.youtube.com/playlist?list=PLAYLIST_ID"
   ```

4. **Extract audio only (MP3)**:

   ```bash
   python app.py --url "https://youtu.be/VIDEO_ID" --audio-only
   ```

5. **Custom output directory**:

   ```bash
   python app.py --url "https://youtu.be/VIDEO_ID" --output /path/to/folder
   ```

6. **Show help**:

   ```bash
   python app.py --help
   ```

Use `-h` or `--help` for a full list of options and flags.

---


---

## 🛡️ License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

This project is licensed under the MIT License.

---

## 👤 Author

**OMKAR SAWANT**

[![GitHub](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/OMI-KALIX)


Made with ❤️ by OMI-KALIX.

> Feel free to contribute! Pull requests and issues are welcome.
>#This project only for Educational purpose
