"""Tests for the server-side migration package target (offline)."""

from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest
from office365.migration.base import MigrationItem
from office365.migration.package import FileSystemStaging
from office365.migration.sharepoint.package_target import SharePointPackageTarget


class _Result:
    def __init__(self, value):
        self.value = value

    def execute_query(self):
        return self


class _Site:
    url = "https://contoso.sharepoint.com/sites/x"

    def __init__(self):
        self.calls: list = []

    def create_migration_ingestion_job(self, **kwargs):
        self.calls.append(("ingestion", kwargs))
        return _Result("job-1")

    def create_migration_job_encrypted(self, **kwargs):
        self.calls.append(("encrypted", kwargs))
        return _Result("job-2")


def _target(tmp_path, site=None, **kwargs):
    return SharePointPackageTarget(
        site or _Site(),
        "web-id",
        content_uri="https://a/content?sig=x",
        manifest_uri="https://a/manifest?sig=y",
        staging=FileSystemStaging(tmp_path / "content", tmp_path / "manifest"),
        **kwargs,
    )


def test_write_accumulates_files_and_folders(tmp_path):
    target = _target(tmp_path)
    target.write(MigrationItem("src/a", "Folder/", item_type="folder"), b"")
    target.write(MigrationItem("src/b", "Folder/b.txt", item_type="file", created="2020-01-01T00:00:00"), b"hi")

    package = target.build()
    root = ET.fromstring(package.manifest)
    assert [o.get("ObjectType") for o in root] == ["Web", "List", "Folder", "File"]
    assert len(package.content) == 1


def test_commit_stages_and_submits(tmp_path):
    site = _Site()
    target = _target(tmp_path, site=site, azure_queue_report_uri="https://a/queue?sig=z")
    target.write(MigrationItem("src/b.txt", "b.txt", item_type="file"), b"hi")

    target.commit()

    assert target.job_id == "job-1"
    kind, kwargs = site.calls[0]
    assert kind == "ingestion"
    assert kwargs["g_web_id"] == "web-id"
    assert kwargs["azure_container_source_uri"] == "https://a/content?sig=x"
    assert kwargs["azure_container_manifest_uri"] == "https://a/manifest?sig=y"
    assert kwargs["azure_queue_report_uri"] == "https://a/queue?sig=z"
    assert (tmp_path / "manifest" / "Manifest.xml").exists()
    assert list((tmp_path / "content").iterdir())  # a content blob was staged


def test_commit_uses_encrypted_submit_with_a_key(tmp_path):
    site = _Site()
    target = _target(tmp_path, site=site, encryption_key=b"secret")
    target.write(MigrationItem("src/b.txt", "b.txt", item_type="file"), b"hi")

    target.commit()

    assert target.job_id == "job-2"
    kind, kwargs = site.calls[0]
    assert kind == "encrypted"
    assert kwargs["aes256_cbc_key"] == b"secret"


def test_target_requires_uris_or_staging():
    with pytest.raises(ValueError, match="required unless staging"):
        SharePointPackageTarget(_Site(), "web-id")


def test_target_stages_to_disk_without_azure(tmp_path):
    target = SharePointPackageTarget(
        _Site(),
        "web-id",
        staging=FileSystemStaging(tmp_path / "content", tmp_path / "manifest"),
    )
    target.write(MigrationItem("src/b.txt", "b.txt", item_type="file"), b"hi")

    package = target.stage()

    assert (tmp_path / "manifest" / "Manifest.xml").exists()
    assert len(package.content) == 1
    with pytest.raises(ValueError, match="required to submit"):
        target.commit()
