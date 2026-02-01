import sys
import subprocess

from config import DOCKER_SERVICE
from decision.paths import canonical_path
from resolvers.apple_music import resolve


def ingest(url: str) -> None:
    tracks = resolve(url)

    for track in tracks:
        path = canonical_path(track)

        if path.exists():
            continue

        path.parent.mkdir(parents=True, exist_ok=True)
        _download(track.url)


def _download(song_url: str) -> None:
    subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            DOCKER_SERVICE,
            "apple-music-dl",
            "--song",
            song_url,
        ],
        check=True,
    )


if __name__ == "__main__":
    ingest(sys.argv[1])
