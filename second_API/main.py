import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from dotenv import load_dotenv
from downloader.youtube import download_youtube_video
from downloader.image import download_image
from downloader.general import download_file
from downloader.social import download_with_ytdlp
from downloader.llm_utils import classify_link_with_llm

load_dotenv()

DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', 'downloads')
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

app = Flask(__name__)
app.config['DOWNLOAD_DIR'] = DOWNLOAD_DIR

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    filename = None
    if request.method == 'POST':
        link = request.form.get('link', '').strip()
        if not link:
            message = 'Please paste a link.'
            return render_template('index.html', message=message)

        # Use LLM to classify the link
        kind = classify_link_with_llm(link)

        try:
            if kind in ('youtube', 'youtube_video') or ('youtube.com' in link or 'youtu.be' in link):
                filename = download_youtube_video(link, DOWNLOAD_DIR)
                message = f'YouTube downloaded: {filename}'
            elif kind == 'image' or link.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                filename = download_image(link, DOWNLOAD_DIR)
                message = f'Image downloaded: {filename}'
            elif kind == 'direct_video' or link.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                filename = download_file(link, DOWNLOAD_DIR)
                message = f'Video downloaded: {filename}'
            elif kind == 'social' or True:
                # Fallback to yt-dlp for many platforms
                filename = download_with_ytdlp(link, DOWNLOAD_DIR)
                message = f'Downloaded via yt-dlp: {filename}'
        except Exception as e:
            message = f'Error: {e}'

        if filename:
            return redirect(url_for('downloaded_file', filename=filename))

    return render_template('index.html', message=message)

@app.route('/downloads/<path:filename>')
def downloaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_DIR'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)