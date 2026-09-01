"""Offline tests for the parallel file transfer and the runner's chunked path."""

from __future__ import annotations

import unittest

from office365.migration.base import ConflictResolution, ItemStatus, MigrationItem, MigrationOptions
from office365.migration.checkpoint import Checkpoint
from office365.migration.runner import MigrationRunner
from office365.migration.transfer import transfer_files_parallel
from office365.runtime.types.event_handler import EventHandler


class _File:
    def execute_query(self):
        return self

    def execute_query_retry(self, **kwargs):
        return self


class _Files:
    def __init__(self, log):
        self._log = log

    def upload(self, content, name):
        self._log.append(("upload", name))
        return _File()

    def create_upload_session(self, path, chunk_size=None, file_name=None):
        self._log.append(("session", file_name))
        return _File()

    def upload_content(self, content, file_name, chunk_size=4 * 1024 * 1024):
        if len(content) <= chunk_size:
            return self.upload(content, file_name)
        return self.create_upload_session(None, chunk_size=chunk_size, file_name=file_name)


class _Folder:
    def __init__(self, context, log):
        self.context = context
        self._log = log
        self._url = "/sites/x/Shared Documents"

    @property
    def server_relative_url(self):
        return self._url

    @property
    def folders(self):
        return self

    def ensure_by_path(self, rel):
        self._log.append(("ensure", rel))
        return self

    def ensure_folder(self, rel):
        return self.ensure_by_path(rel)

    def ensure_folders(self, paths):
        for rel in sorted(set(paths)):
            self.ensure_by_path(rel)
        return self

    @property
    def files(self):
        return _Files(self._log)

    def get(self):
        return self

    def execute_query(self):
        return self


class _Pending:
    beforeExecute = EventHandler()
    afterExecute = EventHandler()
    onError = EventHandler()


class _Context:
    base_url = "https://contoso.sharepoint.com/sites/x"

    def __init__(self, log):
        self._log = log

    def clone(self, url):
        return _Context(self._log)

    def pending_request(self):
        return _Pending()

    @property
    def web(self):
        return self

    def get_folder_by_server_relative_path(self, url):
        return _Folder(self, self._log)


class TestTransferFilesParallel(unittest.TestCase):
    def test_transfers_all_files_and_dedups_folders(self):
        log = []
        root = _Folder(_Context(log), log)
        failures = transfer_files_parallel(
            root,
            [("a.txt", b"x"), ("docs/b.txt", b"y"), ("docs/c.txt", b"z")],
            concurrency=4,
        )

        self.assertEqual(failures, [])
        self.assertEqual(log.count(("ensure", "docs")), 1)  # folder ensured once
        uploads = [entry for entry in log if entry[0] == "upload"]
        self.assertEqual(sorted(name for _, name in uploads), ["a.txt", "b.txt", "c.txt"])

    def test_large_files_use_upload_session(self):
        log = []
        root = _Folder(_Context(log), log)
        big = b"x" * (4 * 1024 * 1024 + 1)
        transfer_files_parallel(root, [("big.bin", big)], concurrency=1)
        self.assertIn(("session", "big.bin"), log)
        self.assertNotIn(("upload", "big.bin"), log)

    def test_empty_input_is_noop(self):
        log = []
        root = _Folder(_Context(log), log)
        self.assertEqual(transfer_files_parallel(root, []), [])
        self.assertEqual(log, [])


class _FakeSource:
    def __init__(self, items):
        self._items = items
        self.payloads = {i.source_path: f"data-{i.source_path}" for i in items}

    def read(self, item):
        return self.payloads[item.source_path]

    def close(self):
        pass


class _FakeTarget:
    def __init__(self):
        self.written = []
        self.batches = []

    def exists(self, item):
        return False

    def write(self, item, payload):
        self.written.append((item.dest_path, payload))

    def write_many(self, items, payloads, concurrency=1):
        self.batches.append(len(items))
        self.written.extend((item.dest_path, payload) for item, payload in zip(items, payloads))
        return []

    def list_paths(self):
        return [p for p, _ in self.written]

    def checksum(self, item):
        return ""

    def commit(self, options=None):
        pass

    def close(self):
        pass


class TestRunnerParallel(unittest.TestCase):
    def _items(self, n: int):
        return [MigrationItem(source_path=f"/s{i}", dest_path=f"f{i}.txt") for i in range(n)]

    def test_parallel_chunks_by_batch_size(self):
        items = self._items(5)
        source = _FakeSource(items)
        target = _FakeTarget()
        options = MigrationOptions(concurrency=2, batch_size=2)
        checkpoint = Checkpoint.create()

        stats = MigrationRunner().run(source, target, items, options, checkpoint)

        self.assertEqual(stats.total, 5)  # noqa: PLR2004
        self.assertEqual(stats.success, 5)  # noqa: PLR2004
        self.assertEqual(stats.errors, 0)
        self.assertEqual(target.batches, [2, 2, 1])  # chunked by batch_size
        statuses = [checkpoint.status_of(i) for i in items]
        self.assertEqual(set(statuses), {ItemStatus.DONE})

    def test_parallel_captures_write_failures(self):
        items = self._items(3)
        source = _FakeSource(items)

        class _Failing(_FakeTarget):
            def write_many(self, items, payloads, concurrency=1):
                return [(items[0].dest_path, "boom")]

        target = _Failing()
        options = MigrationOptions(concurrency=2, batch_size=100)
        stats = MigrationRunner().run(source, target, items, options, Checkpoint.create())

        self.assertEqual(stats.errors, 1)
        self.assertEqual(stats.success, 2)  # noqa: PLR2004
        self.assertEqual(items[0].error, "boom")

    def test_sequential_when_concurrency_is_one(self):
        items = self._items(3)
        source = _FakeSource(items)
        target = _FakeTarget()
        options = MigrationOptions(concurrency=1, conflict_resolution=ConflictResolution.OVERWRITE)
        stats = MigrationRunner().run(source, target, items, options, Checkpoint.create())

        self.assertEqual(stats.success, 3)  # noqa: PLR2004
        self.assertEqual(target.batches, [])  # write_many not used
        self.assertEqual(len(target.written), 3)  # noqa: PLR2004


if __name__ == "__main__":
    unittest.main()
