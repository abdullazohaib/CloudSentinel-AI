"""Tests for the log parser."""

import pytest

from app.domain.logs.parser import LogParser


def test_parse_valid_log() -> None:
    """Parser should convert a valid raw log into structured data."""

    parser = LogParser()

    result = parser.parse(
        "2026-08-10T18:00:00 ERROR Database connection failed"
    )

    assert result.level == "ERROR"
    assert result.message == "Database connection failed"
    assert result.timestamp.isoformat() == "2026-08-10T18:00:00"


def test_parse_lowercase_level() -> None:
    """Parser should normalize the log level."""

    parser = LogParser()

    result = parser.parse(
        "2026-08-10T18:00:05 error Connection timeout"
    )

    assert result.level == "ERROR"


def test_parse_invalid_format() -> None:
    """Parser should reject malformed log lines."""

    parser = LogParser()

    with pytest.raises(ValueError):
        parser.parse("This is not a valid log")


def test_parse_invalid_timestamp() -> None:
    """Parser should reject invalid timestamps."""

    parser = LogParser()

    with pytest.raises(ValueError):
        parser.parse(
            "not-a-timestamp ERROR Database connection failed"
        )