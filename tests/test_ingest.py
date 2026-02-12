"""Tests for ingest module."""
from unittest.mock import patch

from config import COMPOSE_FILE, COMPOSE_PROJECT_DIR, DOCKER_SERVICE
from ingest import _download


def test_download_includes_compose_flags():
    """Test that _download() includes -f and --project-directory flags."""
    test_url = "https://music.apple.com/in/song/test/123456"
    
    with patch("subprocess.run") as mock_run:
        _download(test_url)
        
        # Verify subprocess.run was called
        assert mock_run.called
        
        # Get the command that was passed
        call_args = mock_run.call_args
        command = call_args[0][0]
        
        # Verify it's a list
        assert isinstance(command, list)
        
        # Verify docker compose command structure
        assert command[0] == "docker"
        assert command[1] == "compose"
        assert "-f" in command
        assert "--project-directory" in command
        assert "exec" in command
        assert DOCKER_SERVICE in command
        assert "apple-music-dl" in command
        assert "--song" in command
        assert test_url in command
        
        # Verify compose file path
        f_index = command.index("-f")
        compose_file = command[f_index + 1]
        assert compose_file == str(COMPOSE_FILE)
        
        # Verify project directory
        pd_index = command.index("--project-directory")
        project_dir = command[pd_index + 1]
        assert project_dir == str(COMPOSE_PROJECT_DIR)
        
        # Verify check=True is passed
        assert call_args[1]["check"] is True


def test_download_command_structure():
    """Test the exact command structure matches expected format."""
    test_url = "https://music.apple.com/in/song/test/123456"
    
    with patch("subprocess.run") as mock_run:
        _download(test_url)
        
        call_args = mock_run.call_args
        command = call_args[0][0]
        
        # Expected structure:
        # docker compose -f <file> --project-directory <dir> exec <service> apple-music-dl --song <url>
        expected_parts = [
            "docker",
            "compose",
            "-f",
            str(COMPOSE_FILE),
            "--project-directory",
            str(COMPOSE_PROJECT_DIR),
            "exec",
            DOCKER_SERVICE,
            "apple-music-dl",
            "--song",
            test_url,
        ]
        
        assert command == expected_parts
