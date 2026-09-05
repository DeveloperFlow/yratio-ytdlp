import yt_dlp
from fastapi import Request
from src.utils import pickProxy, getRecommendedHeaders

def extractVideoURL( url: str, request: Request):
    headers = getRecommendedHeaders(url, request)
    options = {
        'http_headers': headers,
        'extract_flat': True,
        'extractor_args': {
            'instagram': {
                'embed': ['true']
            }
        },
        'skip_download': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return {"resp": ydl.extract_info(url, download=False), "proxy": pickProxy()}