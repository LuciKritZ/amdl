"""Tests for docker-compose configuration (Module 2)."""
import subprocess
from pathlib import Path

import pytest

from config import AMDL_ROOT, COMPOSE_FILE, COMPOSE_PROJECT_DIR


def test_compose_file_exists():
    """Compose file must exist under AMDL_ROOT."""
    assert COMPOSE_FILE.exists(), f"Missing {COMPOSE_FILE}"
    assert COMPOSE_FILE.name == "docker-compose.yml"


def test_amdl_wrapper_stub_exists():
    """amdl-wrapper/ must exist with a Dockerfile so compose can build (stub for CI)."""
    wrapper_dir = AMDL_ROOT / "amdl-wrapper"
    dockerfile = wrapper_dir / "Dockerfile"
    assert wrapper_dir.is_dir(), f"Missing {wrapper_dir} (create stub for CI)"
    assert dockerfile.is_file(), f"Missing {dockerfile} (stub required for docker compose build)"


def _docker_compose_config_output():
    """Run docker compose config and return (exit_code, stdout, stderr)."""
    result = subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            str(COMPOSE_FILE),
            "--project-directory",
            str(COMPOSE_PROJECT_DIR),
            "config",
        ],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def _has_docker_compose():
    """Check if docker compose is available."""
    r = subprocess.run(
        ["docker", "compose", "version"],
        capture_output=True,
        text=True,
    )
    return r.returncode == 0


@pytest.mark.skipif(not _has_docker_compose(), reason="docker compose not available")
def test_compose_config_valid_and_services_present():
    """docker compose config must succeed and define services 'wrapper' and 'amdl'."""
    exit_code, stdout, stderr = _docker_compose_config_output()
    assert exit_code == 0, f"docker compose config failed: {stderr!r}\n{stdout!r}"

    # Parse YAML-like output: we only need to assert both service names appear
    out = stdout + "\n" + stderr
    assert "wrapper" in out or "amdl" in out, "Compose output should mention services"
    # Standard compose config output includes service names under "services:"
    assert "wrapper" in stdout, "Service 'wrapper' must be present in compose config"
    assert "amdl" in stdout, "Service 'amdl' must be present in compose config"
