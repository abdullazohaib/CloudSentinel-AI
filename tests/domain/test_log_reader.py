"""Tests for the log reader."""

from pathlib import Path

import pytest

from app.domain.logs.reader import LogReader


def test_read_log_file(tmp_path: Path) -> None:
    """Log reader should return non-empty log lines."""

    log_file = tmp_path / "application.log"

    log_file.write_text(
        "ERROR Database connection failed\n"
        "\n"
        "INFO Retry attempt started\n",
        encoding="utf-8",
    )

    reader = LogReader()

    result = reader.read(str(log_file))

    assert result == [
        "ERROR Database connection failed",
        "INFO Retry attempt started",
    ]


def test_missing_log_file() -> None:
    """Log reader should raise an error for a missing file."""

    reader = LogReader()

    with pytest.raises(FileNotFoundError):
        reader.read("does-not-exist.log")