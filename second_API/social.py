import yt_dlp
import os


def download_with_ytdlp(url: str, out_dir: str = '.') -> str:
    """Use yt-dlp to download from many social platforms. Returns primary filename.
    """
    ydl_opts = {
        'outtmpl': os.path.join(out_dir, '%(title)s-%(id)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    # derive filename
    ext = info.get('ext') or 'mp4'
    title = info.get('title') or 'download'
    id_ = info.get('id') or ''
    filename = f"{title}-{id_}.{ext}".replace('/', '_')
    return filename