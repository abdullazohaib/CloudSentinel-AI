"""Log file reading utilities."""

from pathlib import Path


class LogReader:
    """Reads raw log lines from a local file."""

    def read(self, file_path: str) -> list[str]:
        """Read and return non-empty log lines from a file."""

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Log file not found: {file_path}")

        if not path.is_file():
            raise ValueError(f"Log path is not a file: {file_path}")

        try:
            with path.open("r", encoding="utf-8") as log_file:
                return [
                    line.strip()
                    for line in log_file
                    if line.strip()
                ]
        except OSError as exc:
            raise OSError(
                f"Unable to read log file: {file_path}"
            ) from exc