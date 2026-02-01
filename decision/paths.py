import re
from pathlib import Path

from config import LIBRARY_ROOT
from resolvers.models import Track

_INVALID = re.compile(r'[\\/:*?"<>|]')


def _clean(s: str) -> str:
    return _INVALID.sub("_", s.strip())


def canonical_path(track: Track) -> Path:
    artist = _clean(track.artist)
    album = _clean(track.album)

    track_no = f"{track.track_number:02d}"
    title = _clean(track.song_name)

    return LIBRARY_ROOT / artist / album / f"{track_no} {title}.m4a"
