"""Unit tests for the CheckIt.AI transformation pipeline."""

from checkitai.transformation.pipeline import (
    clean_text,
    determine_image_status,
    determine_label_type,
    normalize_date,
    transform_record,
)


def test_clean_text_removes_extra_whitespace():
    assert clean_text("  Bonjour   le monde  ") == "Bonjour le monde"


def test_clean_text_preserves_none():
    assert clean_text(None) is None


def test_normalize_date_with_timezone():
    result = normalize_date("2026-11-15T04:32:01+00:00")
    assert result == "2026-11-15T04:32:01+00:00"


def test_normalize_date_without_timezone_adds_utc():
    result = normalize_date("2026-11-15 04:32:01")
    assert result == "2026-11-15T04:32:01+00:00"


def test_normalize_date_preserves_missing_value():
    assert normalize_date(None) is None


def test_determine_image_status_without_image():
    record = {"image_url": None, "image_path": None}
    assert determine_image_status(record) == (False, "missing")


def test_determine_image_status_url_only():
    record = {
        "image_url": "https://example.com/image.jpg",
        "image_path": None,
    }
    assert determine_image_status(record) == (False, "url_only")


def test_determine_image_status_downloaded(tmp_path):
    image_file = tmp_path / "image.jpg"
    image_file.write_bytes(b"fake image content")

    record = {
        "image_url": "https://example.com/image.jpg",
        "image_path": str(image_file),
        "image_valid": True,
    }
    assert determine_image_status(record) == (True, "downloaded")


def test_determine_image_status_invalid_file(tmp_path):
    record = {
        "image_url": "https://example.com/image.jpg",
        "image_path": str(tmp_path / "missing.jpg"),
    }
    assert determine_image_status(record) == (False, "invalid")


def test_determine_image_status_rejects_invalid_image():
    record = {
        "image_url": "https://example.com/image.jpg",
        "image_path": "/tmp/image.jpg",
        "image_valid": False,
    }
    assert determine_image_status(record) == (False, "invalid")


def test_determine_label_type_unlabeled():
    record = {"label": None}
    assert determine_label_type(record) == "unlabeled"


def test_determine_label_type_fact_checked():
    record = {"label": "uncertain", "label_status": "fact_checked"}
    assert determine_label_type(record) == "fact_check"


def test_determine_label_type_binary():
    record = {"label": "fake", "label_status": "available"}
    assert determine_label_type(record) == "binary"


def test_transform_record_preserves_original_fields():
    original = {
        "publication_id": "test-001",
        "source_name": "NewsData",
        "title": "  Exemple   de titre  ",
        "text_content": "  Texte   de test. ",
        "image_url": "https://example.com/image.jpg",
        "image_path": None,
        "image_valid": None,
        "label": None,
        "label_status": "unlabeled",
        "published_at": None,
        "collected_at": "2026-11-15 04:32:01",
    }

    result = transform_record(original)

    assert result["publication_id"] == "test-001"
    assert result["title"] == "Exemple de titre"
    assert result["text_content"] == "Texte de test."
    assert result["has_text"] is True
    assert result["has_image"] is False
    assert result["image_status"] == "url_only"
    assert result["label"] is None
    assert result["label_type"] == "unlabeled"
    assert result["published_at"] is None
    assert result["collected_at"] == "2026-11-15T04:32:01+00:00"

    # The original input must not be modified.
    assert original["title"] == "  Exemple   de titre  "
    assert original["label"] is None
