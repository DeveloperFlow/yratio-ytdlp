from fastapi import Request
from urllib.parse import urlparse
from pathlib import Path
import requests
import random
import json
import time

CURRENTDIR = Path(__file__).resolve().parent
POOLCACHEFILE = CURRENTDIR.parent / "var/pool-cache.json"

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
    

#proxy fetching functions
def getFreshProxyPool() -> dict:
    ep = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=json"
    proxies = dict()
    try:
        response = requests.get(ep)
        proxiesData = response.json()
        if isinstance( proxiesData, dict ):
            proxies = proxiesData
    except Exception as e:
        pass
    return proxies

def getCachedProxyPool():
    pool = 0
    if POOLCACHEFILE.is_file():
        try:
            with open(POOLCACHEFILE, "r", encoding = "utf-8") as file:
                pool = json.load(file)
                if isinstance( pool, dict):
                    return pool
        except Exception as e:
            pass
    return None

def refreshProxyPoolCache():
    pool = getFreshProxyPool()
    if "proxies" in pool and isinstance( pool["proxies"], list ):
        with open( POOLCACHEFILE, "w") as file:
            expiration = calcPoolExpiration( pool )
            poolCache = {"expiration": expiration, "pool": pool}
            json.dump( poolCache, file, indent = 4 )
            return poolCache
    return None

def getProxyPool():
    pool = refreshProxyPoolCache()
    if pool:
        expiration = pool["expiration"]
        if time.time() > expiration:
            pool = refreshProxyPoolCache()
    else:
        pool = refreshProxyPoolCache()
    return pool

def getProxyList() -> list:
    pool = getProxyPool()
    proxies = list()
    if isinstance(pool, dict) and "pool" in pool:
        pool = pool["pool"]
        if "proxies" in pool and isinstance( pool["proxies"], list):
            for proxy in pool["proxies"]:
                proxies.append( proxy.get("proxy") )
    return proxies

def pickProxy():
    return "http://tvz9kjec2y2m:i73lfsjaxxgo6fl@45.3.53.7:3129"
    """pool = getProxyList()
    if len( pool ) > 0:
        return random.choice( pool )
    return None"""

def calcPoolExpiration( pool ):
    poolLen = len( pool["proxies"] )
    duration = 3.33 * poolLen
    return int( duration + time.time() )