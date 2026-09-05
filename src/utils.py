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
    BLOCKEDHEADERS = {
        "host",
        "cookie",
        "content-length",
        "content-type",
        "connection",
        "x-forwarded-host",
        "cf-connecting-ip",
        "cf-ray",
        "accept-encoding"
    }
    forwarded = {}
    for key, value in request.headers.items():
        if key.lower() not in BLOCKEDHEADERS:
            forwarded[key] = value
    targetHost = urlparse(url).netloc
    forwarded["Host"] = targetHost
    return forwarded

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
    pool = getCachedProxyPool()
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
    pool = getProxyList()
    if len( pool ) > 0:
        return random.choice( pool )
    return None

def calcPoolExpiration( pool ):
    poolLen = len( pool["proxies"] )
    duration = 3.33 * poolLen
    return int( duration + time.time() )