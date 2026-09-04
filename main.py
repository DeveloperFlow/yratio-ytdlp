from fastapi import FastAPI, HTTPException
import yt_dlp
import requests

app = FastAPI()

@app.get("/extract")
def extract_url(url: str):
    ydl_opts = {
        'extract_flat': True,
        'impersonate': 'chrome:windows',
        'extractor_args': {
            'instagram': {
                'embed': ['true']
            }
        },
        'skip_download': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {"status": "success", "info": info}
    except Exception as e:
        error_msg = str(e) or repr(e) or traceback.format_exc()
        raise HTTPException(status_code=400, detail=error_msg)

@app.get("/test")
def test(url: str):
    HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Host": "www.instagram.com",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
    "X-Forwarded-For": "105.112.39.72",
    "X-Forwarded-Proto": "https",
    "X-Real-Ip": "105.112.39.72"
    }
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))