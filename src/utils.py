from fastapi import Request
from urllib.parse import urlparse
from pathlib import Path
import requests
import random
import json
import time

CURRENTDIR = Path(__file__).resolve().parent
POOLCACHEFILE = CURRENTDIR.parent / "var/proxies.txt"

def getRecommendedHeaders( url: str, request: Request ) -> dict:
    targetHost = urlparse(url).netloc
    referer = request.headers.get("referer")
    clientIP = request.headers.get("true-client-ip")
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
    if referer:
        pass
        #headers["Referer"] = referer
    if clientIP: 
        headers["X-Real-Ip"] = clientIP
        headers["X-Forwarded-For"] = clientIP
    return dict( sorted( headers.items() ) )
    

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
        return random.choice( pool )
    return None

def calcPoolExpiration( pool ):
    poolLen = len( pool["proxies"] )
    duration = 3.33 * poolLen
    return int( duration + time.time() )