
"""Tests simulés des téléchargements HTTP d'images."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from checkitai.extraction.common.image_validator import download_image

CONFIG = {
    "allowed_image_types": [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
    ],
    "max_image_size_mb": 10,
    "request_timeout": 30,
    "max_retries": 1,
    "user_agent": "CheckItAI-Test/0.1",
}


class FakeResponse:
    """Simule une réponse HTTP."""

    def __init__(
        self,
        content: bytes,
        content_type: str,
        status_code: int = 200,
    ) -> None:
        self.content = content
        self.status_code = status_code
        self.headers = {"Content-Type": content_type}
        
        if content:
            self.headers["Content-Length"] = str(len(content))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def iter_content(self, chunk_size=65536):
        yield self.content



@patch(
    "checkitai.extraction.common.image_validator.socket.getaddrinfo",
    return_value=[
        (2, 1, 6, "", ("93.184.216.34", 443))
    ],
)
def main(mock_dns) -> None:
    """Teste les téléchargements simulés."""

    valid_png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 30

    with TemporaryDirectory() as temporary_directory:
        output_dir = Path(temporary_directory)

        print("Test d'un téléchargement PNG valide...")

        with patch(
            "checkitai.extraction.common.image_validator.requests.get",
            return_value=FakeResponse(valid_png, "image/png"),
        ):
            result = download_image(
                url="https://example.com/image.png",
                output_dir=output_dir,
                publication_id="publication_001",
                config=CONFIG,
            )

        assert result["image_valid"] is True
        assert result["download_status"] == "success"

        image_path = Path(result["image_path"])
        assert image_path.exists()
        assert image_path.read_bytes() == valid_png

        print("  OK : image téléchargée et enregistrée")
        print("  Chemin :", image_path)
        print("  Taille :", result["image_size_bytes"], "octets")

        print("\nTest d'un type MIME incorrect...")

        with patch(
            "checkitai.extraction.common.image_validator.requests.get",
            return_value=FakeResponse(
                b"<html>Page web</html>",
                "text/html",
            ),
        ):
            result = download_image(
                url="https://example.com/page",
                output_dir=output_dir,
                publication_id="publication_002",
                config=CONFIG,
            )

        assert result["image_valid"] is False
        assert result["download_status"] == "failed"

        print("  OK : contenu non image rejeté")
        
        print("\nTest HTTP 404 : aucune nouvelle tentative...")

        config_404 = {**CONFIG, "max_retries": 3}

        with patch(
            "checkitai.extraction.common.image_validator.requests.get",
            return_value=FakeResponse(
                b"Not Found",
                "text/plain",
                status_code=404,
            ),
        ) as mock_get:
            result = download_image(
                url="https://example.com/missing.png",
                output_dir=output_dir,
                publication_id="publication_003",
                config=config_404,
            )

        assert result["image_valid"] is False
        assert result["download_status"] == "failed"
        assert result["download_attempts"] == 1
        assert mock_get.call_count == 1

        print("  OK : erreur 404 détectée, une seule requête effectuée")
        
        print("\nTest HTTP 503 : nouvelles tentatives...")

        config_503 = {**CONFIG, "max_retries": 3}

        responses_503 = [
            FakeResponse(b"Service unavailable", "text/plain", 503),
            FakeResponse(b"Service unavailable", "text/plain", 503),
            FakeResponse(b"Service unavailable", "text/plain", 503),
        ]

        with (
            patch(
                "checkitai.extraction.common.image_validator.requests.get",
                side_effect=responses_503,
            ) as mock_get,
            patch(
                "checkitai.extraction.common.image_validator.time.sleep"
            ) as mock_sleep,
        ):
            result = download_image(
                url="https://example.com/temporary-error.png",
                output_dir=output_dir,
                publication_id="publication_004",
                config=config_503,
            )

        assert result["image_valid"] is False
        assert result["download_status"] == "failed"
        assert result["download_attempts"] == 3
        assert mock_get.call_count == 3
        assert mock_sleep.call_count == 2

        print("  OK : erreur 503, trois tentatives effectuées")

        print("\nTous les tests HTTP simulés sont réussis.")


if __name__ == "__main__":
    main()

