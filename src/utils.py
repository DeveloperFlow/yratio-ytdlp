from fastapi import Request
from urllib.parse import urlparse
from pathlib import Path
import requests
import random
import json
import time

CURRENTDIR = Path(__file__).resolve().parent
POOLCACHEFILE = CURRENTDIR.parent / "var/http-proxies.txt"
PLATFORMS = {
    "www.youtube.com": "youtube"
}

def getRecommendedHeaders( url: str, request: Request ) -> dict:
    targetHost = urlparse(url).netloc
    referer = request.headers.get("referer")
    clientIP = request.headers.get("true-client-ip")
    platform = getPlatformFromURL( url )
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": "",
        "Host": targetHost,
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": '"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
        "X-Forwarded-Proto": "https"
    }
    youtubeHeaders = {
        "Priority": "u=0, i",
        "Sec-Ch-Ua-Arch": '"x86"',
        "Sec-Ch-Ua-Bitness": '"64"',
        "Sec-Ch-Ua-Full-Version-List": '"Chromium";v="152.0.7977.77", "Not?A_Brand";v="24.0.0.0", "Google Chrome";v="152.0.7977.77"',
        "Sec-Ch-Ua-Model": '""',
        "Sec-Ch-Ua-Platform-Version": '"10.0.0"',
        "Sec-Ch-Ua-Wow64": "?0",
        "Sec-Fetch-Site": "none"
    }
    if clientIP and platform != "youtube": 
        headers["X-Real-Ip"] = clientIP
        headers["X-Forwarded-For"] = clientIP
        
    if platform == "youtube":
        headers = headers | youtubeHeaders
        del headers["X-Forwarded-Proto"]
    return dict( sorted( headers.items() ) )
    
def getPlatformFromURL( url: str ):
    targetHost = urlparse(url).netloc
    return PLATFORMS.get( targetHost )

def getProxyList():
    proxies = list()
    if POOLCACHEFILE.is_file():
        try:
            with open(POOLCACHEFILE, "r", encoding = "utf-8") as file:
                for line in file:
                    cleanLine = line.rstrip("\n")
                    proxies.append(cleanLine)
        except Exception as e:
            pass
    return proxies

def pickProxy():
    pool = getProxyList()
    if len( pool ) > 0:
        return "http://" + random.choice( pool )
    return None

def calcPoolExpiration( pool ):
    poolLen = len( pool["proxies"] )
    duration = 3.33 * poolLen
    return int( duration + time.time() )