import yt_dlp
from fastapi import Request
from src.utils import pickProxy, getRecommendedHeaders

def extractVideoURL( url: str, request: Request):
    headers = getRecommendedHeaders(url, request)
    options = {
        'http_headers': headers,
        'extract_flat': True,
        'extractor_args': {
            'youtubepot-bgutilhttp': {
                'base_url': 'https://bgutil-usnk.onrender.com'
            }
        },
        'skip_download': True
    }
    proxy = pickProxy()
    if proxy:
        options["proxy"] = proxy
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            return {"result": ydl.extract_info(url, download=False), "proxy": proxy, "headers": headers}
    except Exception as e:
        return {"headers": headers, "proxy": proxy, "error": str(e)}