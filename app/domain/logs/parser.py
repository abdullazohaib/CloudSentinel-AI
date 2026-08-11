"""Log parsing utilities."""

from datetime import datetime

from app.domain.logs.models import ParsedLog


class LogParser:
    """Parse raw log lines into structured log objects."""

    def parse(self, line: str) -> ParsedLog:
        """Parse a single log line."""

        parts = line.split(" ", 2)

        if len(parts) != 3:
            raise ValueError(f"Invalid log format: {line}")

        timestamp_text, level, message = parts

        try:
            timestamp = datetime.fromisoformat(timestamp_text)
        except ValueError as exc:
            raise ValueError(
                f"Invalid timestamp in log: {line}"
            ) from exc

        return ParsedLog(
            timestamp=timestamp,
            level=level.upper(),
            message=message,
        )