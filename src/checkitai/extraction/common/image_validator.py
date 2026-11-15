
"""Validation et téléchargement contrôlé des images distantes."""

from __future__ import annotations

import hashlib
import ipaddress
import logging
import re
import socket
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

LOGGER = logging.getLogger("checkitai.extraction.image_validator")

# Signatures binaires reconnues pour les formats autorisés.
IMAGE_SIGNATURES = {
    "image/jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
    "image/png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    "image/gif": lambda data: data.startswith((b"GIF87a", b"GIF89a")),
    "image/webp": lambda data: (
        len(data) >= 12
        and data[:4] == b"RIFF"
        and data[8:12] == b"WEBP"
    ),
}

IMAGE_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/gif": ".gif",
    "image/webp": ".webp",
}


def _validate_url(url: str) -> None:
    """Vérifie que l'URL utilise HTTP ou HTTPS et possède un hôte."""

    parsed_url = urlparse(url)

    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("Seules les URL HTTP et HTTPS sont autorisées.")

    if not parsed_url.hostname:
        raise ValueError("L'URL ne contient pas de nom d'hôte.")

    if parsed_url.username or parsed_url.password:
        raise ValueError("Les identifiants intégrés dans l'URL sont interdits.")

def _validate_public_host(url: str) -> None:
    """Refuse les hôtes qui résolvent vers des adresses IP non publiques."""

    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port or (
        443 if parsed_url.scheme == "https" else 80
    )

    try:
        addresses = socket.getaddrinfo(
            hostname,
            port,
            type=socket.SOCK_STREAM,
        )
    except OSError as exc:
        raise ValueError(
            f"Impossible de résoudre le nom d'hôte : {hostname}"
        ) from exc

    if not addresses:
        raise ValueError("Aucune adresse IP trouvée pour cet hôte.")

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])

        if not ip.is_global:
            raise ValueError(
                f"Adresse IP non publique interdite : {ip}"
            )


def _validate_signature(content: bytes, content_type: str) -> bool:
    """Vérifie la signature binaire correspondant au type MIME."""

    validator = IMAGE_SIGNATURES.get(content_type)

    return validator(content) if validator else False


def _failure(message: str, attempts: int = 0) -> dict[str, Any]:
    """Construit une réponse standardisée en cas d'échec."""

    return {
        "image_valid": False,
        "image_path": None,
        "image_content_type": None,
        "image_size_bytes": None,
        "download_status": "failed",
        "download_error": message,
        "download_attempts": attempts,
    }


def download_image(
    url: str | None,
    output_dir: str | Path,
    publication_id: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Vérifie et télécharge une image depuis une URL HTTP(S).

    Args:
        url: Adresse distante de l'image.
        output_dir: Répertoire de destination.
        publication_id: Identifiant de la publication associée.
        config: Section ``extraction`` du fichier settings.yaml.

    Returns:
        Dictionnaire décrivant le résultat du téléchargement.
    """

    if not url or not isinstance(url, str):
        return _failure("URL d'image absente ou invalide.")

    try:
        _validate_url(url)
    except ValueError as exc:
        return _failure(str(exc))

    allowed_types = set(config["allowed_image_types"])
    max_size_bytes = int(config["max_image_size_mb"]) * 1024 * 1024
    timeout = int(config["request_timeout"])
    max_retries = int(config["max_retries"])
    user_agent = config["user_agent"]

    if max_size_bytes <= 0:
        return _failure("La taille maximale autorisée doit être positive.")

    if timeout <= 0 or max_retries <= 0:
        return _failure("Le délai et le nombre de tentatives doivent être positifs.")

    safe_id = re.sub(r"[^a-zA-Z0-9_-]", "_", publication_id)

    if not safe_id:
        return _failure("Identifiant de publication invalide.")

    url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]

    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    attempts = 0
    last_error = "Échec du téléchargement."

    for attempt in range(1, max_retries + 1):
        attempts = attempt
        temporary_file: Path | None = None

        try:
            response = requests.get(
                url,
                headers={"User-Agent": user_agent},
                timeout=timeout,
                stream=True,
                allow_redirects=False,
            )

            with response:
                if response.status_code != 200:
                    raise requests.HTTPError(
                        f"Réponse HTTP inattendue : {response.status_code}",
                        response=response,
                    )

                content_type = (
                    response.headers.get("Content-Type", "")
                    .split(";")[0]
                    .strip()
                    .lower()
                )

                if content_type not in allowed_types:
                    raise ValueError(
                        f"Type MIME non autorisé : {content_type or 'absent'}"
                    )

                extension = IMAGE_EXTENSIONS.get(content_type)

                if extension is None:
                    raise ValueError("Extension d'image non prise en charge.")

                content_length = response.headers.get("Content-Length")

                if content_length:
                    try:
                        declared_size = int(content_length)
                    except ValueError as exc:
                        raise ValueError(
                            "En-tête Content-Length invalide."
                        ) from exc

                    if declared_size < 0 or declared_size > max_size_bytes:
                        raise ValueError(
                            "Taille annoncée supérieure à la limite autorisée."
                        )

                temporary_file = (
                    destination / f".{safe_id}_{url_hash}.part"
                )

                downloaded_size = 0
                first_chunk = b""

                with temporary_file.open("wb") as file:
                    for chunk in response.iter_content(chunk_size=64 * 1024):
                        if not chunk:
                            continue

                        downloaded_size += len(chunk)

                        if downloaded_size > max_size_bytes:
                            raise ValueError(
                                "Image supérieure à la taille maximale autorisée."
                            )

                        if len(first_chunk) < 32:
                            first_chunk += chunk[: 32 - len(first_chunk)]

                        file.write(chunk)

                if not _validate_signature(first_chunk, content_type):
                    raise ValueError(
                        "La signature binaire ne correspond pas au type MIME."
                    )

                final_file = (
                    destination / f"{safe_id}_{url_hash}{extension}"
                )

                temporary_file.replace(final_file)
                temporary_file = None

                LOGGER.info(
                    "Image téléchargée : publication=%s, taille=%s octets",
                    publication_id,
                    downloaded_size,
                )

                return {
                    "image_valid": True,
                    "image_path": str(final_file),
                    "image_content_type": content_type,
                    "image_size_bytes": downloaded_size,
                    "download_status": "success",
                    "download_error": None,
                    "download_attempts": attempts,
                }

        except (requests.RequestException, ValueError, OSError) as exc:
            last_error = str(exc)

            LOGGER.warning(
                "Échec téléchargement image (%s/%s) pour %s : %s",
                attempt,
                max_retries,
                publication_id,
                last_error,
            )

            if isinstance(exc, requests.HTTPError) and exc.response is not None:
                retryable_statuses = {408, 425, 429, 500, 502, 503, 504}

                if exc.response.status_code not in retryable_statuses:
                    return _failure(last_error, attempt)

        finally:
            if temporary_file is not None:
                temporary_file.unlink(missing_ok=True)

        if attempt < max_retries:
            time.sleep(min(2 ** (attempt - 1), 8))

    return _failure(last_error, attempts)

