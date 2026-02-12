# AMDL - Apple Music Downloader

Deterministic Apple Music → ALAC ingestion tool.

## Overview

AMDL downloads Apple Music tracks and converts them to ALAC format. It uses Docker Compose to orchestrate the wrapper and downloader services.

**Note:** An active Apple Music subscription is required.

## Disclaimer

This tool is for **educational purposes only** and does not intend to violate any legalities. Users are responsible for ensuring they comply with Apple Music's Terms of Service and applicable copyright laws. The developers assume no liability for misuse of this software.

For concerns or issues, contact: **hi@krishalshah.in**

## Configuration

### AMDL_ROOT

Root directory for amdl (defaults to directory containing `config.py`). Override via:

```bash
export AMDL_ROOT=/path/to/amdl
```

### Docker Compose

Compose file: `AMDL_ROOT/docker-compose.yml`  
Project directory: `AMDL_ROOT`

## Running

```bash
python amdl/ingest.py <url>
```

With shell integration (Module 5):

```bash
amdl playlist|album|song <url>
```

## Development

### Running Tests

```bash
cd amdl
PYTHONPATH=. uv run pytest tests/ -v
```

### Project Structure

- `amdl/` - Main module directory
  - `config.py` - Configuration (includes `AMDL_ROOT`, compose paths)
  - `ingest.py` - Main ingestion logic
  - `docker-compose.yml` - Docker Compose configuration (to be added in Module 2)
  - `tests/` - Test suite

## Credits

This project builds upon the excellent work of:

- **[WorldObservationLog/wrapper](https://github.com/WorldObservationLog/wrapper)** - Apple Music decryption wrapper
- **[zhaarey/apple-music-downloader](https://github.com/zhaarey/apple-music-downloader)** - Apple Music ALAC/Dolby Atmos/AAC/MV downloader
