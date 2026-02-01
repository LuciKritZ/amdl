import os
from pathlib import Path
from typing import Final

try:
    from dotenv import load_dotenv

    _project_root = Path(__file__).parent
    _env_file = _project_root / ".env"
    if _env_file.exists():
        load_dotenv(_env_file)
except ImportError:
    # python-dotenv not installed, skip .env file loading
    pass


def _get_path(env_var: str, default: Path) -> Path:
    """Get path from environment variable or use default.
    
    Args:
        env_var: Environment variable name
        default: Default Path object
        
    Returns:
        Path object from env var or default
    """
    value = os.getenv(env_var)
    if value:
        return Path(value).expanduser().resolve()
    return default


def _get_int(env_var: str, default: int) -> int:
    """Get integer from environment variable or use default.
    
    Args:
        env_var: Environment variable name
        default: Default integer value
        
    Returns:
        Integer from env var or default
    """
    value = os.getenv(env_var)
    if value:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"{env_var} must be a valid integer, got: {value}")
    return default


def _get_str(env_var: str, default: str) -> str:
    """Get string from environment variable or use default.
    
    Args:
        env_var: Environment variable name
        default: Default string value
        
    Returns:
        String from env var or default
    """
    return os.getenv(env_var, default)


# Library Configuration
LIBRARY_ROOT: Final[Path] = _get_path(
    "AMDL_LIBRARY_ROOT",
    Path("/mnt/Krishal/apple-music"),
)

# Authentication Configuration
COOKIES_PATH: Final[Path] = _get_path(
    "AMDL_COOKIES_PATH",
    Path.home() / ".config" / "gamdl" / "cookies.txt",
)

CACHE_PATH: Final[Path] = _get_path(
    "AMDL_CACHE_PATH",
    Path.home() / ".cache" / "amdl" / "developer_token.json",
)

TOKEN_TTL: Final[int] = _get_int(
    "AMDL_TOKEN_TTL",
    5 * 60 * 60,  # 5 hours in seconds
)

# Apple Music API Configuration
STOREFRONT: Final[str] = _get_str(
    "AMDL_STOREFRONT",
    "in",
)

# Docker Configuration
DOCKER_SERVICE: Final[str] = _get_str(
    "AMDL_DOCKER_SERVICE",
    "amdl",
)

# Apple Music API Constants (not configurable, but kept here for reference)
APPLE_MUSIC_HOMEPAGE_URL: Final[str] = "https://music.apple.com"
APPLE_MUSIC_COOKIE_DOMAIN: Final[str] = ".music.apple.com"
APPLE_MUSIC_API: Final[str] = "https://amp-api.music.apple.com/v1/catalog/{storefront}"

