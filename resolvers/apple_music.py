import re
import requests

from auth.apple_music_web_token import get_token, get_cookies
from .models import Track


APPLE_MUSIC_API = "https://amp-api.music.apple.com/v1/catalog/{storefront}"
STOREFRONT = "in"


SONG_RE = re.compile(r"/song/[^/]+/(\d+)")
ALBUM_RE = re.compile(r"/album/[^/]+/(\d+)")
PLAYLIST_RE = re.compile(r"/playlist/[^/]+/(pl\.[^/?]+)")

def _headers() -> dict:
    return {
        "Authorization": f"Bearer {get_token()}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Origin": "https://music.apple.com",
        "Referer": "https://music.apple.com/",
    }

def resolve(url: str) -> list[Track]:
    kind, identifier = _classify(url)

    if kind == "song":
        return [_resolve_song(identifier)]
    if kind == "album":
        return _resolve_album(identifier)
    if kind == "playlist":
        return _resolve_playlist(identifier)

    raise RuntimeError("unreachable")


def _classify(url: str) -> tuple[str, str]:
    if m := SONG_RE.search(url):
        return "song", m.group(1)
    if m := ALBUM_RE.search(url):
        return "album", m.group(1)
    if m := PLAYLIST_RE.search(url):
        return "playlist", m.group(1)

    raise ValueError(f"Unsupported Apple Music URL: {url}")


def _resolve_song(song_id: str) -> Track:
    data = _fetch(f"/songs/{song_id}")["data"][0]
    return _track(data)


def _resolve_album(album_id: str) -> list[Track]:
    data = _fetch(f"/albums/{album_id}")["data"][0]
    tracks = data["relationships"]["tracks"]["data"]
    return _normalize(tracks)


def _resolve_playlist(playlist_id: str) -> list[Track]:
    data = _fetch(f"/playlists/{playlist_id}")["data"][0]
    tracks = data["relationships"]["tracks"]["data"]
    return _normalize(tracks)


def _normalize(items: list[dict]) -> list[Track]:
    tracks = [_track(t) for t in items]
    return sorted(tracks, key=lambda t: (t.disc_number, t.track_number))


def _track(song: dict) -> Track:
    attrs = song["attributes"]

    return Track(
        song_id=song["id"],
        song_name=attrs["name"],
        artist=attrs["artistName"],
        album=attrs.get("albumName") or attrs["name"],
        disc_number=int(attrs.get("discNumber", 1)),
        track_number=int(attrs.get("trackNumber", 0)),
        url=attrs["url"],
    )


def _fetch(path: str) -> dict:
    url = APPLE_MUSIC_API.format(storefront=STOREFRONT) + path
    cookies = get_cookies()
    # Only send media-user-token cookie
    cookies_dict = {"media-user-token": cookies["media-user-token"]}
    resp = requests.get(url, headers=_headers(), cookies=cookies_dict)
    resp.raise_for_status()
    return resp.json()
