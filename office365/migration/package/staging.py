"""Content staging — put a package's blobs where the Migration API can read them.

Staging is the **swappable seam** between the vendor-neutral package (documented
XML + content blobs) and the transport SharePoint's ingestion service reads from.
Two strategies are provided:

- :class:`FileSystemStaging` — writes blobs under a directory (offline/testing, or
  a staging area for a later upload) — **no Azure**;
- :class:`BlobStaging` — uploads to the content/manifest containers (requires the
  ``[azure]`` extra: ``pip install office365-rest-python-client[azure]``); with an
  ``encryption_key`` every blob is AES-256-CBC encrypted (SharePoint-provided
  containers require this).

:func:`create_staging` picks a strategy from the container URLs; it is the
extension point for a future S3 / Azure Files staging.

Content and manifest blobs go to **different** containers — the API rejects a job
whose content and manifest containers match.
"""

from __future__ import annotations

import base64
import importlib
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from office365.migration.package.crypto import decrypt, encrypt, normalize_key

if TYPE_CHECKING:
    from office365.migration.package.builder import Package

__all__ = ["AzureBlobStaging", "BlobStaging", "FileSystemStaging", "Staging", "create_staging"]

_AZURE_EXTRA_HINT = "Azure staging requires the 'azure' extra: pip install office365-rest-python-client[azure]"

# Azure Blob hosts (public cloud + US Government).
_AZURE_BLOB_HOSTS = ("blob.core.windows.net", "blob.core.usgovcloudapi.net")


class Staging:
    """Strategy that places a package's content + manifest blobs for ingestion."""

    def stage(self, package: "Package") -> None:
        raise NotImplementedError


class FileSystemStaging(Staging):
    """Writes the package's blobs under ``content_dir`` / ``manifest_dir``."""

    def __init__(self, content_dir: str | Path, manifest_dir: str | Path | None = None) -> None:
        self._content_dir = Path(content_dir)
        self._manifest_dir = Path(manifest_dir) if manifest_dir is not None else self._content_dir / "manifest"

    @property
    def content_dir(self) -> Path:
        return self._content_dir

    @property
    def manifest_dir(self) -> Path:
        return self._manifest_dir

    def stage(self, package: "Package") -> None:
        self._content_dir.mkdir(parents=True, exist_ok=True)
        self._manifest_dir.mkdir(parents=True, exist_ok=True)
        for name, data in package.content.items():
            (self._content_dir / name).write_bytes(data)
        for name, data in package.blobs().items():
            (self._manifest_dir / name).write_bytes(data)


class BlobStaging(Staging):
    """Uploads the package's blobs to the content/manifest Azure Blob containers.

    The container URIs must embed a SAS token (e.g. the ``DataContainerUri`` /
    ``MetadataContainerUri`` returned by ``Site.provision_migration_containers``).
    A snapshot is created for every content blob, as the API requires.

    Pass ``encryption_key`` (the base64 ``EncryptionKey`` from
    ``provision_migration_containers``) for SharePoint-provided containers: every
    content and manifest blob is then AES-256-CBC encrypted, with its base64 IV
    stored as the ``IV`` blob property.
    """

    def __init__(
        self,
        content_uri: str,
        manifest_uri: str,
        encryption_key: str | bytes | None = None,
    ) -> None:
        if content_uri.rstrip("?") == manifest_uri.rstrip("?"):
            raise ValueError("content and manifest containers must differ")
        self._content_uri = content_uri
        self._manifest_uri = manifest_uri
        self._key = normalize_key(encryption_key) if encryption_key else None

    def stage(self, package: "Package") -> None:
        container_client = _container_client()
        content = container_client.from_container_url(self._content_uri)
        manifest = container_client.from_container_url(self._manifest_uri)
        for name, data in package.content.items():
            blob = content.get_blob_client(name)
            self._upload(blob, data)
            blob.create_snapshot()  # the API reads the latest snapshot
        for name, data in package.blobs().items():
            self._upload(manifest.get_blob_client(name), data)

    def _upload(self, blob, data: bytes) -> None:
        if self._key is None:
            blob.upload_blob(data, overwrite=True)
            return
        ciphertext, iv = encrypt(data, self._key)
        blob.upload_blob(ciphertext, overwrite=True, metadata={"IV": iv})

    def read_manifest_blob(self, name: str) -> bytes:
        """Download a blob (e.g. the API's import log) from the manifest container.

        Provisioned containers grant ``Read`` (not ``List``), so the caller must
        know the blob name — ``JobLogFileCreate`` events carry it. The containers
        are AES-256-CBC encrypted end-to-end, so the API's own logs come back as
        ciphertext; with a key set they are decrypted using the blob's ``IV``
        metadata (falling back to a 16-byte IV prefixed to the payload).
        """
        blob = _container_client().from_container_url(self._manifest_uri).get_blob_client(name)
        data = blob.download_blob().readall()
        if self._key is None:
            return data
        iv = _blob_iv(blob)
        if iv is None and len(data) > 16:  # noqa: PLR2004
            iv = base64.b64encode(data[:16]).decode("ascii")
            data = data[16:]
        if iv is None:
            return data
        try:
            return decrypt(data, self._key, iv)
        except Exception:  # noqa: BLE001 — not encrypted with our key; return raw
            return data


# Back-compat alias (the class was introduced as ``AzureBlobStaging``).
AzureBlobStaging = BlobStaging


def create_staging(
    content_url: str,
    manifest_url: str,
    encryption_key: str | bytes | None = None,
) -> Staging:
    """Return a :class:`Staging` for the given container URLs.

    Azure Blob is the only backend today (the SharePoint Migration API requires it
    for the server-side ingest leg). This factory is the extension point: a future
    S3 / Azure Files staging can be selected here by URL host without changing
    callers.
    """
    host = urlparse(content_url).hostname or ""
    if host.endswith(_AZURE_BLOB_HOSTS):
        return BlobStaging(content_url, manifest_url, encryption_key=encryption_key)
    raise ValueError(
        f"unsupported staging container host {host!r}: only Azure Blob ({', '.join(_AZURE_BLOB_HOSTS)}) is supported"
    )


def _container_client():
    """Lazily import ``azure.storage.blob.ContainerClient`` (optional extra)."""
    try:
        module = importlib.import_module("azure.storage.blob")
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise ImportError(_AZURE_EXTRA_HINT) from exc
    return module.ContainerClient


def _blob_iv(blob) -> str | None:
    """The base64 ``IV`` from a blob's metadata, when present."""
    try:
        metadata = blob.get_blob_properties().metadata or {}
    except Exception:  # noqa: BLE001 — metadata is best-effort
        return None
    return next((value for key, value in metadata.items() if key.lower() == "iv"), None)
