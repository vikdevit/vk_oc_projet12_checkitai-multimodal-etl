
import pytest

from checkitai.extraction.common.image_validator import (
    IMAGE_SIGNATURES,
    _failure,
    _validate_signature,
    _validate_url,
)


@pytest.mark.parametrize(
    ("content_type", "content"),
    [
        ("image/jpeg", b"\xff\xd8\xff\xe0" + b"\x00" * 20),
        ("image/png", b"\x89PNG\r\n\x1a\n" + b"\x00" * 20),
        ("image/gif", b"GIF89a" + b"\x00" * 20),
        ("image/webp", b"RIFF" + b"\x00" * 4 + b"WEBP" + b"\x00" * 20),
    ],
)
def test_validate_signature_accepts_supported_images(content_type, content):
    assert _validate_signature(content, content_type)


def test_validate_signature_rejects_html():
    assert not _validate_signature(
        b"<html>Page web</html>",
        "image/jpeg",
    )


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/image.jpg",
        "http://example.com/image.png",
    ],
)
def test_validate_url_accepts_http_urls(url):
    _validate_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.com/image.jpg",
        "file:///etc/passwd",
        "https:///image.jpg",
    ],
)
def test_validate_url_rejects_invalid_urls(url):
    with pytest.raises(ValueError):
        _validate_url(url)


def test_failure_returns_structured_result():
    result = _failure("URL absente")

    assert result["image_valid"] is False
    assert result["image_path"] is None
    assert result["download_status"] == "failed"


def test_image_signatures_are_defined():
    assert "image/jpeg" in IMAGE_SIGNATURES
    assert "image/png" in IMAGE_SIGNATURES
    assert "image/gif" in IMAGE_SIGNATURES
    assert "image/webp" in IMAGE_SIGNATURES

