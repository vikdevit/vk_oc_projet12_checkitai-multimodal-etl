
"""Tests locaux des fonctions de validation des images."""

from checkitai.extraction.common.image_validator import (
    IMAGE_SIGNATURES,
    _failure,
    _validate_signature,
    _validate_url,
)


def main() -> None:
    """Teste les signatures binaires et les URL."""

    print("Test des signatures d'images...")

    samples = {
        "image/jpeg": b"\xff\xd8\xff\xe0" + b"\x00" * 20,
        "image/png": b"\x89PNG\r\n\x1a\n" + b"\x00" * 20,
        "image/gif": b"GIF89a" + b"\x00" * 20,
        "image/webp": b"RIFF" + b"\x00" * 4 + b"WEBP" + b"\x00" * 20,
    }

    for content_type, content in samples.items():
        assert _validate_signature(content, content_type)
        print(f"  OK : {content_type}")

    assert not _validate_signature(
        b"<html>Page web</html>",
        "image/jpeg",
    )
    print("  OK : rejet d'un contenu HTML")

    print("\nTest des URL...")

    valid_urls = [
        "https://example.com/image.jpg",
        "http://example.com/image.png",
    ]

    for url in valid_urls:
        _validate_url(url)
        print(f"  OK : {url}")

    invalid_urls = [
        "ftp://example.com/image.jpg",
        "file:///etc/passwd",
        "https:///image.jpg",
    ]

    for url in invalid_urls:
        try:
            _validate_url(url)
        except ValueError:
            print(f"  OK : URL rejetée ({url})")
        else:
            raise AssertionError(f"URL qui aurait dû être rejetée : {url}")

    print("\nTest de la réponse d'échec...")

    result = _failure("URL absente")

    assert result["image_valid"] is False
    assert result["image_path"] is None
    assert result["download_status"] == "failed"

    print("  OK : réponse d'échec structurée")

    print("\nTous les tests locaux sont réussis.")
    print("Formats reconnus :", ", ".join(IMAGE_SIGNATURES))


if __name__ == "__main__":
    main()

