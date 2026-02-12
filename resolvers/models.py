from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    song_id: str
    song_name: str
    artist: str
    album_artist: str
    album: str
    disc_number: int
    disc_total: int
    track_number: int
    compilation: bool
    url: str
