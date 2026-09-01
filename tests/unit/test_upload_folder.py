"""Offline tests for the sequential, deferred ``MoveCopyUtil.upload_folder``."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.utilities.move_copy_util import MoveCopyUtil


def _folder() -> Folder:
    ctx = ClientContext("https://contoso.sharepoint.com/sites/x")
    return ctx.web.root_folder


class TestUploadFolderEntries(unittest.TestCase):
    def test_directory_walk_preserves_structure(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "docs").mkdir()
            (root / "docs" / "a.txt").write_text("alpha")
            (root / "b.txt").write_text("beta")

            entries = MoveCopyUtil._collect_upload_entries(root, recursive=True)
            rels = sorted(rel for rel, _ in entries)
            self.assertEqual(rels, ["b.txt", "docs/a.txt"])
            self.assertEqual(dict(entries)["docs/a.txt"](), b"alpha")
            self.assertEqual(dict(entries)["b.txt"](), b"beta")

    def test_directory_walk_non_recursive_is_flat(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "docs").mkdir()
            (root / "docs" / "a.txt").write_text("alpha")
            (root / "b.txt").write_text("beta")

            entries = MoveCopyUtil._collect_upload_entries(root, recursive=False)
            self.assertEqual([rel for rel, _ in entries], ["b.txt"])

    def test_single_file_uses_name(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write("hello")
            path = Path(f.name)
        try:
            entries = MoveCopyUtil._collect_upload_entries(path, recursive=True)
            self.assertEqual([rel for rel, _ in entries], [path.name])
        finally:
            path.unlink()

    def test_list_of_file_paths_each_at_name(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            a = root / "a.txt"
            a.write_text("a")
            b = root / "b.txt"
            b.write_text("b")

            entries = MoveCopyUtil._collect_upload_entries([a, b], recursive=True)
            self.assertEqual(sorted(rel for rel, _ in entries), ["a.txt", "b.txt"])

    def test_content_pairs(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.bin"
            p.write_bytes(b"\x01\x02")
            entries = MoveCopyUtil._collect_upload_entries(
                [("f.txt", b"bytes"), ("t.txt", "text"), ("p.bin", p)],
                recursive=True,
            )
            by_rel = dict(entries)
            self.assertEqual(by_rel["f.txt"](), b"bytes")
            self.assertEqual(by_rel["t.txt"](), b"text")
            self.assertEqual(by_rel["p.bin"](), b"\x01\x02")


class _FakeFile:
    def __init__(self, name: str) -> None:
        self.name = name

    def after_execute(self, fn):
        return self


class TestUploadFolderChain(unittest.TestCase):
    def test_chain_uploads_in_order_with_progress(self):
        folder = _folder()
        callbacks = []  # (relative_path, after_execute_fn) as the chain registers them
        seen_progress = []
        uploaded_files = []

        def _fake_upload(rel, content, chunk_size=4 * 1024 * 1024):
            fake = _FakeFile(rel)
            orig = fake.after_execute

            def _capture(fn):
                callbacks.append((rel, fn))
                return orig(fn)

            fake.after_execute = _capture
            return fake

        with mock.patch.object(folder, "upload_file", side_effect=_fake_upload):
            result = MoveCopyUtil.upload_folder(
                folder,
                [("a.txt", b"a"), ("docs/b.txt", b"b")],
                after_file_uploaded=lambda f: uploaded_files.append(f.name),
                progress=lambda p: seen_progress.append(p.done),
            )
            self.assertEqual(result, folder)
            self.assertEqual(len(callbacks), 1)  # first upload queued, chain not driven

            while callbacks:  # drive the deferred chain FIFO
                _rel, fn = callbacks.pop(0)
                fn(_FakeFile(_rel))

        self.assertEqual(seen_progress, [1, 2])  # noqa: PLR2004
        self.assertEqual(uploaded_files, ["a.txt", "docs/b.txt"])

    def test_empty_source_is_noop(self):
        folder = _folder()
        with mock.patch.object(folder, "upload_file") as upload:
            result = MoveCopyUtil.upload_folder(folder, [])
            self.assertEqual(result, folder)
            upload.assert_not_called()


if __name__ == "__main__":
    unittest.main()
