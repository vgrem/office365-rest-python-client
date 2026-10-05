"""Stream Microsoft Graph usage reports straight to a file or binary stream.

The reports endpoints return CSV (or JSON) by first replying with a short-lived
``302 Found`` whose ``Location`` points at a pre-authenticated download URL. The
existing query helpers (``get_email_activity_user_detail`` and friends) fetch the
body into memory as ``bytes``, which is fine for a few thousand rows but wasteful
for the tenant-wide ``*Detail`` reports that run into hundreds of thousands.

:func:`download_report` / :func:`download_report_async` build the same request,
follow the redirect through the normal transport (auth, pacing, proxies) and
stream the response into a path or an already-open binary stream, so the whole
report never sits in memory at once. The bytes written and the server-provided
file name (from ``Content-Disposition``) are returned as a
:class:`ReportExportResult`.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass
from email.message import Message
from typing import IO, TYPE_CHECKING, Iterator, Mapping, Optional, Union

import requests

from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.operations import ProgressCallback, emit_progress
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.transport.base import DEFAULT_STREAM_CHUNK_SIZE

if TYPE_CHECKING:
    from office365.reports.root import ReportRoot
    from office365.runtime.client_request import ClientRequest
    from office365.runtime.http.request_options import RequestOptions

#: Where :func:`download_report` sends the report: a filesystem path or any
#: writable binary stream.
ReportTarget = Union[str, "os.PathLike[str]", IO[bytes]]


@dataclass
class ReportExportResult:
    """The outcome of a streamed report download.

    Attributes:
        file_name: Server-provided file name from ``Content-Disposition`` when the
            service supplies one, else ``None``.
        bytes_written: Number of body bytes written to the target.
    """

    file_name: Optional[str]
    bytes_written: int


@contextmanager
def _open_target(target: ReportTarget) -> Iterator[IO[bytes]]:
    """Yield a writable binary stream, opening (and closing) a path if needed."""
    if isinstance(target, (str, os.PathLike)):
        with open(target, "wb") as file_object:
            yield file_object
    else:
        yield target


def _truncate(file_object: IO[bytes]) -> None:
    """Rewind a seekable target so a re-download does not leave trailing bytes."""
    seekable = getattr(file_object, "seekable", None)
    if callable(seekable) and seekable():
        file_object.seek(0)
        file_object.truncate()


def _filename_from_headers(headers: Mapping[str, str]) -> Optional[str]:
    """Extract ``filename`` from a ``Content-Disposition`` header, if present."""
    disposition = headers.get("Content-Disposition")
    if not disposition:
        return None
    message = Message()
    message["Content-Disposition"] = disposition
    return message.get_filename()


def _build_download_request(
    report_root: "ReportRoot", report_name: str, period: Optional[str]
) -> "tuple[ClientRequest, RequestOptions]":
    """Build a streaming GET for a report (auth is applied by the caller)."""
    pending = report_root.context.pending_request()
    query = FunctionQuery(report_root, report_name, {"period": period}, None, return_raw_content=True)
    request = pending.build_request(query)
    request.stream = True
    return pending, request


class _ChunkTracker:
    """Collects ``Content-Length`` / file name and counts streamed bytes."""

    def __init__(self, file_object: IO[bytes], progress: Optional[ProgressCallback]) -> None:
        self.bytes_written = 0
        self.file_name: Optional[str] = None
        self.total: Optional[int] = None
        self._file_object = file_object
        self._progress = progress

    def on_headers(self, headers: Mapping[str, str]) -> None:
        length = headers.get("Content-Length")
        self.total = int(length) if length else None
        self.file_name = _filename_from_headers(headers)

    def write(self, chunk: bytes) -> None:
        if not chunk:
            return
        self.bytes_written += len(chunk)
        emit_progress(self._progress, done=self.bytes_written, total=self.total, stage="downloading")
        self._file_object.write(chunk)


def download_report(
    report_root: "ReportRoot",
    report_name: str,
    target: ReportTarget,
    period: Optional[str] = None,
    *,
    chunk_size: int = DEFAULT_STREAM_CHUNK_SIZE,
    progress: Optional[ProgressCallback] = None,
) -> ReportExportResult:
    """Stream a usage report to ``target`` (blocking).

    Args:
        report_root: The report container (``client.reports``).
        report_name: The Graph function name, e.g. ``"getTeamsUserActivityUserDetail"``.
        target: A filesystem path or a writable binary stream.
        period: Aggregation period (``D7``, ``D30``, ``D90``, ``D180``) for the
            ``*UserDetail`` reports.
        chunk_size: Number of bytes read per chunk.
        progress: Optional ``ProgressCallback`` invoked per chunk.

    Returns:
        A :class:`ReportExportResult` with the bytes written and the server's
        file name.

    Raises:
        ClientRequestException: When the service returns an error status.
    """
    pending, request = _build_download_request(report_root, report_name, period)
    pending.beforeExecute(request)
    with _open_target(target) as file_object:
        _truncate(file_object)
        tracker = _ChunkTracker(file_object, progress)
        try:
            for chunk in pending.transport.stream(request, chunk_size=chunk_size, on_headers=tracker.on_headers):
                tracker.write(chunk)
        except requests.HTTPError as ex:
            error = ClientRequestException.from_response(ex.response)
            if pending.onError:
                pending.onError(error)
                return ReportExportResult(file_name=None, bytes_written=tracker.bytes_written)
            raise error from ex
    return ReportExportResult(file_name=tracker.file_name, bytes_written=tracker.bytes_written)


async def download_report_async(
    report_root: "ReportRoot",
    report_name: str,
    target: ReportTarget,
    period: Optional[str] = None,
    *,
    chunk_size: int = DEFAULT_STREAM_CHUNK_SIZE,
    progress: Optional[ProgressCallback] = None,
) -> ReportExportResult:
    """Async twin of :func:`download_report` that never blocks the event loop.

    Streams through the configured async transport — native when one is set
    (e.g. :class:`~office365.runtime.transport.httpx_transport.HttpxTransport`),
    otherwise a worker thread — so the loop stays free and the report is never
    buffered in memory.
    """
    pending, request = _build_download_request(report_root, report_name, period)
    await pending.before_execute_async(request)
    with _open_target(target) as file_object:
        _truncate(file_object)
        tracker = _ChunkTracker(file_object, progress)
        try:
            async for chunk in pending.async_transport.stream_async(
                request, chunk_size=chunk_size, on_headers=tracker.on_headers
            ):
                tracker.write(chunk)
        except requests.HTTPError as ex:
            error = ClientRequestException.from_response(ex.response)
            if pending.onError:
                pending.onError(error)
                return ReportExportResult(file_name=None, bytes_written=tracker.bytes_written)
            raise error from ex
    return ReportExportResult(file_name=tracker.file_name, bytes_written=tracker.bytes_written)


__all__ = ["ReportExportResult", "ReportTarget", "download_report", "download_report_async"]
