from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/extract")
def extract_url(url: str):
    ydl_opts = {'extract_flat': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {"status": "success", "url": info.get("url")}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))