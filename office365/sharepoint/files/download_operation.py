"""High-level bulk download: one ``download(...)`` builder, one awaitable terminal.

The low-level queue primitives (``ctx.execute_query_parallel(_async)``) own the
fan-out, but the caller still has to open destination streams, keep them alive
across the await, and derive local paths. :class:`DownloadOperation` hides all of
that: ``Folder.download(...)`` / ``FileCollection.download(...)`` /
``File.download(path)`` return an operation whose terminal
(``execute_query()`` / ``await execute_query_async()``) enumerates, opens and
closes the destinations, drains the downloads with bounded concurrency, and
populates :attr:`DownloadOperation.value` with a :class:`DownloadResult`.

Domain intent stays on the builder (``recursive``, ``overwrite``, ``progress``);
execution knobs stay on the terminal (``concurrency``, retry), mirroring
``execute_query_parallel``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple, Union

from typing_extensions import Self

from office365.runtime.operations import OperationStats, ProgressCallback, query_progress_hook
from office365.sharepoint.thresholds import SAFE_PAGE_SIZE

if TYPE_CHECKING:
    from office365.runtime.client_runtime_context import ClientRuntimeContext
    from office365.sharepoint.files.collection import FileCollection
    from office365.sharepoint.files.file import File
    from office365.sharepoint.folders.folder import Folder

_PathLike = Union[str, Path]
_FilePair = Tuple["File", str]


@dataclass
class DownloadResult:
    """Outcome of a :class:`DownloadOperation` run.

    Attributes:
        paths: Local paths written by successful downloads, in completion order.
        stats: ``total`` (files discovered), ``success``, ``skipped`` (already
          present and ``overwrite=False``), ``errors`` counters.
        failures: ``(file, error)`` pairs for downloads that permanently failed;
          the rest of the batch still runs.
    """

    paths: List[str] = field(default_factory=list)
    stats: OperationStats = field(default_factory=OperationStats)
    failures: List[Tuple["File", BaseException]] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.stats.total

    @property
    def success(self) -> int:
        return self.stats.success

    @property
    def skipped(self) -> int:
        return self.stats.skipped

    @property
    def errors(self) -> int:
        return self.stats.errors

    def raise_if_errors(self) -> "DownloadResult":
        """Re-raise the first permanent failure, when any file failed."""
        if self.failures:
            raise self.failures[0][1]
        return self

    def __bool__(self) -> bool:
        return not self.failures


class _Plan:
    """Resolves the work into ``(file, relative_path)`` pairs at execution time."""

    def resolve(self) -> List[_FilePair]:
        raise NotImplementedError

    async def resolve_async(self) -> List[_FilePair]:
        raise NotImplementedError


class _FolderPlan(_Plan):
    """Enumerate a folder (optionally recursive) via the paged ``get_files``."""

    def __init__(self, folder: "Folder", *, recursive: bool, scan_progress: Optional[ProgressCallback]) -> None:
        self._folder = folder
        self._recursive = recursive
        self._scan_progress = scan_progress

    def _enumerate(self) -> "FileCollection":
        self._folder.ensure_property("ServerRelativeUrl")
        return self._folder.get_files(recursive=self._recursive, progress=self._scan_progress)

    def resolve(self) -> List[_FilePair]:
        col = self._enumerate()
        col.execute_query()
        return _pairs(col, self._folder.server_relative_url)

    async def resolve_async(self) -> List[_FilePair]:
        col = self._enumerate()
        await col.execute_query_async()
        return _pairs(col, self._folder.server_relative_url)


class _CollectionPlan(_Plan):
    """Use the collection's loaded items, or page the folder when not loaded."""

    def __init__(self, collection: "FileCollection", *, scan_progress: Optional[ProgressCallback]) -> None:
        self._collection = collection
        self._scan_progress = scan_progress

    def _enumerate(self) -> "FileCollection":
        col = self._collection
        col.parent.ensure_property("ServerRelativeUrl")
        if len(col) == 0:
            col.get_all(page_size=SAFE_PAGE_SIZE, progress=self._scan_progress)
        return col

    def resolve(self) -> List[_FilePair]:
        col = self._enumerate()
        col.execute_query()
        return _pairs(col, col.parent.server_relative_url)

    async def resolve_async(self) -> List[_FilePair]:
        col = self._enumerate()
        await col.execute_query_async()
        return _pairs(col, col.parent.server_relative_url)


class _FilePlan(_Plan):
    """A single, already-addressed file."""

    def __init__(self, file: "File") -> None:
        self._file = file

    def resolve(self) -> List[_FilePair]:
        if self._file.context.has_pending_request:
            self._file.context.execute_query()
        return [(self._file, "")]

    async def resolve_async(self) -> List[_FilePair]:
        if self._file.context.has_pending_request:
            await self._file.context.execute_query_async()
        return [(self._file, "")]


def _relative(url: Optional[str], root_url: Optional[str]) -> str:
    """Path of ``url`` relative to ``root_url`` (basename fallback)."""
    if not url:
        return ""
    if root_url:
        root = root_url.rstrip("/") + "/"
        if url.startswith(root):
            return url[len(root) :]
        if url == root_url:
            return ""
    return os.path.basename(url.rstrip("/"))


def _pairs(col: "FileCollection", root_url: Optional[str]) -> List[_FilePair]:
    """Map a loaded :class:`FileCollection` to ``(file, relative_path)`` pairs."""
    pairs: List[_FilePair] = []
    for file in col:
        rel = _relative(file.server_relative_url, root_url)
        if not rel:
            rel = file.name or ""
        pairs.append((file, rel))
    return pairs


def _write_bytes(dest: Path, content: bytes) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as stream:  # noqa: ASYNC230 - local, brief, off the network
        stream.write(content)


class DownloadOperation:
    """A deferred bulk download, driven by ``execute_query`` / ``execute_query_async``.

    Created by the ``download`` builders; not instantiated directly.
    """

    def __init__(
        self,
        context: "ClientRuntimeContext",
        plan: _Plan,
        *,
        target_dir: Optional[_PathLike] = None,
        dest_file: Optional[_PathLike] = None,
        overwrite: bool = False,
        progress: Optional[ProgressCallback] = None,
        on_file: Optional[Callable[["File"], None]] = None,
    ) -> None:
        self._context = context
        self._plan = plan
        self._target_dir = Path(target_dir) if target_dir is not None else None
        self._dest_file = Path(dest_file) if dest_file is not None else None
        self._overwrite = overwrite
        self._progress = progress
        self._on_file = on_file
        self._value: Optional[DownloadResult] = None

    @property
    def value(self) -> DownloadResult:
        """The outcome of the run, populated by a terminal.

        Raises:
            ValueError: if accessed before ``execute_query`` /
                ``execute_query_async``.
        """
        if self._value is None:
            raise ValueError("DownloadOperation has not been executed yet")
        return self._value

    @classmethod
    def for_folder(
        cls,
        folder: "Folder",
        target_dir: _PathLike,
        *,
        recursive: bool = True,
        overwrite: bool = False,
        progress: Optional[ProgressCallback] = None,
    ) -> "DownloadOperation":
        return cls(
            folder.context,
            _FolderPlan(folder, recursive=recursive, scan_progress=progress),
            target_dir=target_dir,
            overwrite=overwrite,
            progress=progress,
        )

    @classmethod
    def for_collection(
        cls,
        collection: "FileCollection",
        target_dir: _PathLike,
        *,
        overwrite: bool = False,
        progress: Optional[ProgressCallback] = None,
    ) -> "DownloadOperation":
        return cls(
            collection.context,
            _CollectionPlan(collection, scan_progress=progress),
            target_dir=target_dir,
            overwrite=overwrite,
            progress=progress,
        )

    @classmethod
    def for_file(
        cls,
        file: "File",
        dest: _PathLike,
        *,
        overwrite: bool = False,
        on_file: Optional[Callable[["File"], None]] = None,
        progress: Optional[ProgressCallback] = None,
    ) -> "DownloadOperation":
        return cls(
            file.context,
            _FilePlan(file),
            dest_file=dest,
            overwrite=overwrite,
            progress=progress,
            on_file=on_file,
        )

    def execute_query(
        self,
        *,
        concurrency: int = 4,
        max_retry: int = 5,
        timeout_secs: int = 5,
        max_delay: Optional[int] = None,
        jitter: bool = True,
    ) -> Self:
        """Download synchronously (bounded concurrency, continue-and-report).

        Returns this operation; the outcome is available on :attr:`value`.
        """
        pairs = self._plan.resolve()
        self._value = self._run_sync(
            pairs,
            concurrency=concurrency,
            max_retry=max_retry,
            timeout_secs=timeout_secs,
            max_delay=max_delay,
            jitter=jitter,
        )
        return self

    async def execute_query_async(
        self,
        *,
        concurrency: int = 4,
        max_retry: int = 5,
        timeout_secs: int = 5,
        max_delay: Optional[int] = None,
        jitter: bool = True,
    ) -> Self:
        """Download without blocking the event loop (bounded concurrency).

        Returns this operation; the outcome is available on :attr:`value`.
        """
        pairs = await self._plan.resolve_async()
        self._value = await self._run_async(
            pairs,
            concurrency=concurrency,
            max_retry=max_retry,
            timeout_secs=timeout_secs,
            max_delay=max_delay,
            jitter=jitter,
        )
        return self

    def _prepare(self, pairs: List[_FilePair]) -> Tuple[List[Tuple["File", Path]], DownloadResult]:
        result = DownloadResult()
        todo: List[Tuple["File", Path]] = []
        for file, rel in pairs:
            dest = self._dest_file if self._dest_file is not None else self._target_dir / rel  # type: ignore[operator]
            result.stats.total += 1
            if not self._overwrite and dest.exists():
                result.stats.skipped += 1
                continue
            todo.append((file, dest))
        return todo, result

    def _queue(self, file: "File", dest: Path, result: DownloadResult) -> object:
        return_type = file.get_content()

        def _save(rt) -> None:
            _write_bytes(dest, rt.value)
            result.paths.append(str(dest))
            result.stats.success += 1
            if callable(self._on_file):
                self._on_file(file)

        return_type.after_execute(_save)
        return return_type

    def _collector(self, owners: dict, result: DownloadResult) -> Callable:
        def _on_error(qry, error: BaseException) -> None:
            result.stats.errors += 1
            file = owners.get(id(qry.return_type))
            if file is not None:
                result.failures.append((file, error))

        return _on_error

    def _progress_hook(self, total: int) -> Optional[Callable]:
        if not callable(self._progress):
            return None
        return query_progress_hook(total, self._progress, stage="downloading")

    def _windows(self, todo: List[Tuple["File", Path]], concurrency: int) -> List[List[Tuple["File", Path]]]:
        size = max(1, concurrency)
        return [todo[index : index + size] for index in range(0, len(todo), size)]

    def _run_sync(
        self,
        pairs: List[_FilePair],
        *,
        concurrency: int,
        max_retry: int,
        timeout_secs: int,
        max_delay: Optional[int],
        jitter: bool,
    ) -> DownloadResult:
        todo, result = self._prepare(pairs)
        progress = self._progress_hook(len(todo))
        for window in self._windows(todo, concurrency):
            owners: dict = {}
            for file, dest in window:
                owners[id(self._queue(file, dest, result))] = file
            self._context.execute_query_parallel(
                concurrency=max(1, concurrency),
                progress=progress,
                max_retry=max_retry,
                timeout_secs=timeout_secs,
                max_delay=max_delay,
                jitter=jitter,
                on_error=self._collector(owners, result),
            )
        return result

    async def _run_async(
        self,
        pairs: List[_FilePair],
        *,
        concurrency: int,
        max_retry: int,
        timeout_secs: int,
        max_delay: Optional[int],
        jitter: bool,
    ) -> DownloadResult:
        todo, result = self._prepare(pairs)
        progress = self._progress_hook(len(todo))
        for window in self._windows(todo, concurrency):
            owners: dict = {}
            for file, dest in window:
                owners[id(self._queue(file, dest, result))] = file
            await self._context.execute_query_parallel_async(
                concurrency=max(1, concurrency),
                progress=progress,
                max_retry=max_retry,
                timeout_secs=timeout_secs,
                max_delay=max_delay,
                jitter=jitter,
                on_error=self._collector(owners, result),
            )
        return result
