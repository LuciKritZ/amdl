import re
from pathlib import Path

from config import LIBRARY_ROOT
from resolvers.models import Track

_INVALID = re.compile(r'[\\/:*?"<>|;]')


def _clean(s: str) -> str:
    return _INVALID.sub("_", s.strip())


def canonical_path(track: Track) -> Path:
    if track.album:
        if track.compilation:
            folder_parts = ["Compilations", _clean(track.album)]
        else:
            folder_parts = [_clean(track.album_artist), _clean(track.album)]
    else:
        folder_parts = [_clean(track.artist), "Unknown Album"]

    title = _clean(track.song_name)
    if track.disc_total > 1:
        file_stem = f"{track.disc_number}-{track.track_number:02d} {title}"
    else:
        file_stem = f"{track.track_number:02d} {title}"

    return LIBRARY_ROOT.joinpath(*folder_parts, f"{file_stem}.m4a")
