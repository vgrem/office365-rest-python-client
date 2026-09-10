"""Parallel file transfer into a SharePoint document library (adapter-internal).

Unlike the library's **deferred** upload primitives (``upload_folder`` /
``upload_file`` / ``upload_content`` — single context, sequential, queue-then-
execute), a transfer is the **concurrent driver** over them: file bytes can't
ride an OData batch, so throughput comes from concurrency. This module is a thin
specialization of the generic :func:`~office365.runtime.parallel.run_parallel`
primitive — each worker uploads on a cloned ``ClientContext`` (reusing the
source's auth + transport, thread-safe) and all workers pace *together* through
the shared :class:`RateLimiter` the primitive wires up.

Folders are created once (deduplicated) before transferring; the per-file upload
delegates to the library's size-dispatching :meth:`FileCollection.upload_content`.

Internal: consumed by :class:`SharePointLibraryTarget.write_many`.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Tuple

from office365.runtime.parallel import run_parallel

if TYPE_CHECKING:
    from office365.sharepoint.folders.folder import Folder

_DEFAULT_CHUNK_SIZE = 4 * 1024 * 1024

# runtime-evaluated alias (typing form: the ``|``/``tuple[...]`` operators need 3.9+)
Failure = Tuple[str, str]  # (dest_path, error)


def _transfer_files_parallel(
    target_folder: "Folder",
    files: Iterable[tuple[str, bytes]],
    *,
    concurrency: int = 4,
    progress: Callable | None = None,
    chunk_size: int = _DEFAULT_CHUNK_SIZE,
    context_factory: Callable | None = None,
) -> list[Failure]:
    """Transfer ``(dest_path, content)`` pairs into a library folder tree in parallel.

    Folders are ensured once each (deduplicated); files at or below ``chunk_size``
    use the simple ``upload``, larger ones a resumable ``create_upload_session``
    (both via :meth:`FileCollection.upload_content`). All workers share one
    :class:`RateLimiter`, so throttling pauses the group as a whole.

    Args:
        target_folder: Root target folder (``server_relative_url`` must be loaded).
        files: Iterable of ``(relative_path, content_bytes)``.
        concurrency: Number of parallel transfer workers.
        progress: Optional hook fired per transferred file with a ``Progress`` snapshot.
        chunk_size: Upload-session chunk size / size threshold (bytes).
        context_factory: Optional per-worker context provider (defaults to a
          ``ClientContext.clone`` of ``target_folder.context``).

    Returns:
        List of ``(dest_path, error)`` for files that failed (empty on success).
    """
    files = list(files)
    if not files:
        return []
    root_url = (target_folder.server_relative_url or "").rstrip("/")
    if not root_url:
        raise ValueError("target folder must expose its server-relative URL")

    parents = {dest.rsplit("/", 1)[0] for dest, _ in files if "/" in dest}
    if parents:
        target_folder.ensure_folders(parents).execute_query()

    failures: list[Failure] = []
    context_factory = context_factory or (lambda: target_folder.context.clone(target_folder.context.base_url))

    def _worker(clone, item: tuple[str, bytes]) -> None:
        dest_path, content = item
        parts = dest_path.split("/")
        name = parts[-1]
        parent_url = f"{root_url}/{'/'.join(parts[:-1])}" if len(parts) > 1 else root_url
        folder = clone.web.get_folder_by_server_relative_path(parent_url)
        folder.files.upload_content(content, name, chunk_size).execute_query_retry(max_retry=5)

    run_parallel(
        _worker,
        files,
        concurrency=concurrency,
        context_factory=context_factory,
        progress=progress,
        on_error=lambda item, error: failures.append((item[0], str(error))),
    )
    return failures
