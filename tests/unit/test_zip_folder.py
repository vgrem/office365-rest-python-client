"""Offline tests for the zip <-> folder primitives (download_folder_as_zip alias, upload_folder_from_zip)."""

from __future__ import annotations

import io
import unittest
import zipfile
from unittest import mock

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.utilities.move_copy_util import MoveCopyUtil


def _folder() -> Folder:
    ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
    return ctx.web.root_folder


def _zip_stream() -> io.BytesIO:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("docs/a.txt", "alpha")
        zf.writestr("b.csv", "1,2")
        zf.writestr("empty/", "")  # directory entry — must be skipped
    buffer.seek(0)
    return buffer


class _FakeFile:
    def __init__(self, name: str) -> None:
        self.name = name

    def after_execute(self, fn):
        return self


class TestUploadFolderFromZip(unittest.TestCase):
    def test_uploads_literal_entries_in_order(self):
        folder = _folder()
        callbacks = []
        seen_progress = []
        uploaded = []

        def _fake_upload(rel, content, chunk_size=4 * 1024 * 1024):
            fake = _FakeFile(rel)
            orig = fake.after_execute

            def _capture(fn):
                callbacks.append((rel, fn))
                return orig(fn)

            fake.after_execute = _capture
            return fake

        with mock.patch.object(folder, "upload_file", side_effect=_fake_upload):
            result = MoveCopyUtil.upload_folder_from_zip(
                folder,
                _zip_stream(),
                after_file_uploaded=lambda f: uploaded.append(f.name),
                progress=lambda p: seen_progress.append(p.done),
            )
            self.assertEqual(result, folder)
            self.assertEqual(len(callbacks), 1)  # first entry queued; chain not driven

            while callbacks:  # drive the deferred chain FIFO
                rel, fn = callbacks.pop(0)
                fn(_FakeFile(rel))

        # literal paths in order; directory entries skipped
        self.assertEqual(uploaded, ["b.csv", "docs/a.txt"])
        self.assertEqual(seen_progress, [1, 2])  # noqa: PLR2004

    def test_empty_zip_is_noop(self):
        folder = _folder()
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w"):
            pass
        buffer.seek(0)
        with mock.patch.object(folder, "upload_file") as upload:
            MoveCopyUtil.upload_folder_from_zip(folder, buffer)
            upload.assert_not_called()

    def test_download_folder_alias_delegates(self):
        folder = _folder()
        with mock.patch.object(MoveCopyUtil, "download_folder_as_zip") as impl:
            impl.return_value = folder
            MoveCopyUtil.download_folder(folder, io.BytesIO())
            impl.assert_called_once()


if __name__ == "__main__":
    unittest.main()
