"""Ollama client integration."""

import requests

from app.core.config import settings


class OllamaClient:
    """Client for communicating with a local Ollama server."""

    def __init__(
        self,
        host: str | None = None,
        model: str | None = None,
    ) -> None:
        self.host = (
            host or settings.ollama_host
        ).rstrip("/")

        self.model = (
            model or settings.ollama_model
        )

    def generate(self, prompt: str) -> str:
        """Generate a response from Ollama.

        Returns an empty string when Ollama is unavailable or
        returns an invalid response so the caller can use its
        fallback behavior.
        """

        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=60,
            )

            response.raise_for_status()

            data = response.json()

            return str(
                data.get("response", "")
            ).strip()

        except (
            requests.RequestException,
            ValueError,
            TypeError,
        ):
            return ""