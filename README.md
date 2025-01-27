YouTube Downloader Flask App
This is a simple Flask app that allows users to download YouTube videos in various formats and qualities. The app supports both video and audio downloads, with the ability to select the audio bitrate when downloading in MP3 format.

Features
Video Download: Choose your preferred video quality and download YouTube videos.
Audio Download: Download YouTube videos as MP3 files with adjustable audio bitrate.
Easy-to-use Interface: A simple web interface where users can input a YouTube URL and choose the download options.
Requirements
Python 3.6+
Flask
yt-dlp
FFmpeg (for audio processing)
Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/omi-kalix/project.git
cd yt-downloader
Create a virtual environment (optional but recommended):

bash
Copy
Edit
python -m venv venv
Activate the virtual environment:

On Windows:
bash
Copy
Edit
venv\Scripts\activate
On macOS/Linux:
bash
Copy
Edit
source venv/bin/activate
Install the required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
The requirements.txt file should contain:

Copy
Edit
Flask
yt-dlp
Install FFmpeg:

Windows: Download from FFmpeg website and add it to your system path.
macOS: Install via Homebrew:
bash
Copy
Edit
brew install ffmpeg
Linux: Install via your package manager, e.g., on Ubuntu:
bash
Copy
Edit
sudo apt-get install ffmpeg
Configure FFmpeg path (if necessary): If FFmpeg is installed in a custom location, make sure to update the ffmpeg_location in app.py:

python
Copy
Edit
options['ffmpeg_location'] = r'C:\ffmpeg\bin'  # Adjust this path as necessary
Running the App
Start the Flask server:

bash
Copy
Edit
python app.py
Access the app in your browser:

Open http://127.0.0.1:5000 in your web browser.
Usage
Enter a YouTube URL: Paste the URL of the YouTube video you want to download.
Select Format: Choose between MP3 or Video.
For MP3 downloads, you can adjust the Audio Bitrate.
For video downloads, select the Video Quality (higher quality requires more bandwidth).
Click Download: After entering the details, click the "Download" button to start the download process.
Folder Structure
php
Copy
Edit
yt-downloader/
├── app.py              # Main Flask app
├── downloads/          # Folder where the downloaded files will be saved
├── requirements.txt    # List of dependencies
├── templates/
│   └── index.html      # Frontend template for the app
└── static/             # (Optional) Static files (e.g., CSS, JS)
Troubleshooting
Missing FFmpeg: Make sure FFmpeg is properly installed and accessible via the system path.
Invalid URL: Ensure that the YouTube URL is valid and correctly formatted.
Audio bitrate error: Ensure you enter a valid bitrate value (e.g., 128, 192, 256).
License
This project is open-source and available under the MIT License.

