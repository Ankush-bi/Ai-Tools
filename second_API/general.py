import requests
import os
from urllib.parse import urlparse


def download_file(url: str, out_dir: str = '.') -> str:
    r = requests.get(url, stream=True)
    r.raise_for_status()
    path = urlparse(url).path
    name = os.path.basename(path) or 'file'
    filename = os.path.join(out_dir, name)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*16):
            if chunk:
                f.write(chunk)
    return os.path.basename(filename)