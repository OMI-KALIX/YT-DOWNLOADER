from flask import Flask, render_template, request, send_file
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.mkdir(DOWNLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url")
    format_choice = request.form.get("format")
    quality_choice = request.form.get("quality")
    audio_bitrate = request.form.get("audio_bitrate")  # New field for audio bitrate
    
    if not url:
        return "Error: URL is required!", 400
    
    options = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'ffmpeg_location': r'C:\ffmpeg\bin',  # Adjust this path as necessary
    }
    
    if format_choice == "mp3":
        options['format'] = f'bestaudio[abr<={audio_bitrate}]'  # Use selected audio bitrate
        options['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': audio_bitrate,
        }]
    else:
        options['format'] = f'bestvideo[height<={quality_choice}]+bestaudio/best'

    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_choice == "mp3":
                filename = filename.replace(".webm", ".mp3")
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)