from pytube import YouTube
import os


def download_youtube_video(url: str, out_dir: str = '.') -> str:
    """Download a YouTube video using pytube and return filename."""
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    if not stream:
        stream = yt.streams.get_highest_resolution()
    out_path = stream.download(output_path=out_dir)
    filename = os.path.basename(out_path)
    return filename