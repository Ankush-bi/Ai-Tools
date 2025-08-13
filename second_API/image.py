import requests
import os
from urllib.parse import urlparse


def download_image(url: str, out_dir: str = '.') -> str:
    r = requests.get(url, stream=True)
    r.raise_for_status()
    path = urlparse(url).path
    name = os.path.basename(path) or 'image'
    # ensure extension
    if not os.path.splitext(name)[1]:
        # try to get from headers
        ct = r.headers.get('content-type', '')
        if 'jpeg' in ct:
            name += '.jpg'
        elif 'png' in ct:
            name += '.png'
    filename = os.path.join(out_dir, name)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(1024):
            if chunk:
                f.write(chunk)
    return os.path.basename(filename)