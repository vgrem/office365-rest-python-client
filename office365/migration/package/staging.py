"""Content staging — put a package's blobs where the Migration API can read them.

Staging is the **swappable seam** between the vendor-neutral package (documented
XML + content blobs) and the transport SharePoint's ingestion service reads from.
Two strategies are provided:

- :class:`FileSystemStaging` — writes blobs under a directory (offline/testing, or
  a staging area for a later upload) — **no Azure**;
- :class:`BlobStaging` — uploads to the content/manifest containers (requires the
  ``[azure]`` extra: ``pip install office365-rest-python-client[azure]``).

:func:`create_staging` picks a strategy from the container URLs; it is the
extension point for a future S3 / Azure Files staging.

Content and manifest blobs go to **different** containers — the API rejects a job
whose content and manifest containers match.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

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
    """

    def __init__(self, content_uri: str, manifest_uri: str) -> None:
        if content_uri.rstrip("?") == manifest_uri.rstrip("?"):
            raise ValueError("content and manifest containers must differ")
        self._content_uri = content_uri
        self._manifest_uri = manifest_uri

    def stage(self, package: "Package") -> None:
        container_client = _container_client()
        content = container_client.from_container_url(self._content_uri)
        manifest = container_client.from_container_url(self._manifest_uri)
        for name, data in package.content.items():
            blob = content.get_blob_client(name)
            blob.upload_blob(data, overwrite=True)
            blob.create_snapshot()  # the API reads the latest snapshot
        for name, data in package.blobs().items():
            manifest.get_blob_client(name).upload_blob(data, overwrite=True)


# Back-compat alias (the class was introduced as ``AzureBlobStaging``).
AzureBlobStaging = BlobStaging


def create_staging(content_url: str, manifest_url: str) -> Staging:
    """Return a :class:`Staging` for the given container URLs.

    Azure Blob is the only backend today (the SharePoint Migration API requires it
    for the server-side ingest leg). This factory is the extension point: a future
    S3 / Azure Files staging can be selected here by URL host without changing
    callers.
    """
    host = urlparse(content_url).hostname or ""
    if host.endswith(_AZURE_BLOB_HOSTS):
        return BlobStaging(content_url, manifest_url)
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
