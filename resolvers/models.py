from dataclasses import dataclass


@dataclass(frozen=True)
class Track:
    song_id: str
    song_name: str
    artist: str
    album: str
    disc_number: int
    track_number: int
    url: str
