import json
import re
import time
import requests
from http.cookiejar import MozillaCookieJar

from config import (
    APPLE_MUSIC_COOKIE_DOMAIN,
    APPLE_MUSIC_HOMEPAGE_URL,
    CACHE_PATH,
    COOKIES_PATH,
    TOKEN_TTL,
)


def get_cookies() -> dict:
    """Load cookies from Netscape format file and return as dictionary."""
    jar = MozillaCookieJar()
    jar.load(COOKIES_PATH, ignore_discard=True, ignore_expires=True)

    cookies = {
        c.name: c.value
        for c in jar
        if c.domain == APPLE_MUSIC_COOKIE_DOMAIN
    }

    if "media-user-token" not in cookies:
        raise RuntimeError("media-user-token not found in cookies.txt")

    return cookies


def _get_token_from_homepage() -> str:
    """Extract developer token from Apple Music homepage JavaScript."""
    # Fetch homepage
    resp = requests.get(APPLE_MUSIC_HOMEPAGE_URL, timeout=15)
    resp.raise_for_status()
    home_page = resp.text

    # Find index.js URI
    index_js_uri_match = re.search(
        r"/(assets/index-legacy[~-][^/\"]+\.js)",
        home_page,
    )
    if not index_js_uri_match:
        raise Exception("index.js URI not found in Apple Music homepage")
    index_js_uri = index_js_uri_match.group(1)

    # Fetch index.js
    resp = requests.get(f"{APPLE_MUSIC_HOMEPAGE_URL}/{index_js_uri}", timeout=15)
    resp.raise_for_status()
    index_js_page = resp.text

    # Extract JWT token (starts with "eyJh")
    token_match = re.search(r'(?=eyJh)(.*?)(?=")', index_js_page)
    if not token_match:
        raise Exception("Token not found in index.js page")
    token = token_match.group(1)

    return token


def get_token() -> str:
    """Get developer token (cached or fetched from homepage)."""
    # Check cache
    if CACHE_PATH.exists():
        data = json.loads(CACHE_PATH.read_text())
        if time.time() - data["ts"] < TOKEN_TTL:
            return data["token"]

    # Fetch new token
    token = _get_token_from_homepage()

    # Cache it
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(
        json.dumps(
            {
                "token": token,
                "ts": int(time.time()),
            }
        )
    )

    return token
