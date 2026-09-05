from fastapi import FastAPI, HTTPException, Request
import requests
from src.utils import getRecommendedHeaders
from src.downloader import extractVideoURL

app = FastAPI()

@app.get("/extract")
def extractURL(url: str, request: Request):
    try:
        info = extractVideoURL( url, request )
        return {"status": "success", "info": info}
    except Exception as e:
        error_msg = str(e) or repr(e) or traceback.format_exc()
        raise HTTPException(status_code=400, detail=error_msg)

@app.get("/test")
def test(url: str, request: Request):
    Headers = getRecommendedHeaders( request, url )
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        return {
            "status_code": response.status_code,
            "request_headers": Headers,
            "headers": dict(response.headers),
            "body": response.text
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))