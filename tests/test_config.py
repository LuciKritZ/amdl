"""Tests for config module."""
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from config import AMDL_ROOT, COMPOSE_FILE, COMPOSE_PROJECT_DIR


def test_amdl_root_default():
    """Test that AMDL_ROOT defaults to config.py's parent directory."""
    # AMDL_ROOT should be the directory containing config.py
    expected_root = Path(__file__).parent.parent
    assert AMDL_ROOT == expected_root
    assert AMDL_ROOT.is_dir()


def test_amdl_root_from_env():
    """Test that AMDL_ROOT can be overridden via environment variable."""
    with tempfile.TemporaryDirectory() as tmpdir:
        custom_root = Path(tmpdir) / "custom_amdl"
        custom_root.mkdir()
        
        with patch.dict(os.environ, {"AMDL_ROOT": str(custom_root)}):
            # Need to reload config to pick up env var
            # For this test, we'll just verify the path resolution logic
            from config import _get_path
            resolved = _get_path("AMDL_ROOT", Path(__file__).parent.parent)
            assert resolved == custom_root.resolve()


def test_compose_file_derived_from_amdl_root():
    """Test that COMPOSE_FILE is derived from AMDL_ROOT."""
    assert COMPOSE_FILE == AMDL_ROOT / "docker-compose.yml"
    assert COMPOSE_FILE.parent == AMDL_ROOT


def test_compose_project_dir_equals_amdl_root():
    """Test that COMPOSE_PROJECT_DIR equals AMDL_ROOT."""
    assert COMPOSE_PROJECT_DIR == AMDL_ROOT
