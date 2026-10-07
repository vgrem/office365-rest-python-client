from __future__ import annotations

import hashlib
import io
import os
import tempfile
import uuid
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, Callable, Optional, Union, cast

from office365.runtime.operations import Progress, ProgressCallback
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.transport.offload import get_offload_executor, run_offloaded
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.files.creation_information import FileCreationInformation
from office365.sharepoint.files.file import File
from office365.sharepoint.files.publish.status import FileStatus
from office365.sharepoint.pages.template_file_type import TemplateFileType
from office365.sharepoint.thresholds import LIST_VIEW_THRESHOLD, Limits, ensure_within, limit
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath

if TYPE_CHECKING:
    from office365.sharepoint.files.download_operation import DownloadOperation
    from office365.sharepoint.folders.folder import Folder

_DEFAULT_CHUNK_SIZE = Limits.UPLOAD_SESSION_CHUNK.value  # simple-upload threshold / upload-session chunk


def _stream_size(stream: IO) -> int:
    """Byte length of a seekable stream (file or ``io.BytesIO``), preserving position.

    Raises:
        ValueError: When the upload source is not seekable.
    """
    pos = stream.tell()
    try:
        stream.seek(0, io.SEEK_END)
        return stream.tell()
    except OSError as e:
        raise ValueError("Upload source must be a seekable file or stream") from e
    finally:
        try:
            stream.seek(pos)
        except OSError:
            pass


class FileCollection(EntityCollection[File]):
    """Represents a collection of File resources."""

    _list_view_threshold = LIST_VIEW_THRESHOLD
    _truncation_hint = "page it with Folder.get_files(page_size=2000) or files.get_all(page_size=2000)"

    def __init__(
        self,
        context: ClientContext,
        resource_path: Optional[ResourcePath] = None,
        parent: Optional[Folder] = None,
    ) -> None:
        super().__init__(context, File, resource_path, parent)

    def get_published_file(self, base_file_path: str) -> FileStatus:
        """ """
        return_type = FileStatus(self.context)
        qry = ServiceOperationQuery(self, "GetPublishedFile", [base_file_path], None, None, return_type)
        self.context.add_query(qry)
        return return_type

    def upload(self, path_or_file: Union[str, IO], file_name: Optional[str] = None) -> File:
        """Uploads a file into folder.

        Note: This method only supports files up to 4MB in size!
        Consider create_upload_session method instead for larger files

        Args:
            path_or_file (str or typing.IO): Path where file to upload resides or file handle
            file_name (str): New file name
        """
        if isinstance(path_or_file, str):
            with open(path_or_file, "rb") as f:
                content = f.read()
            name = file_name or os.path.basename(path_or_file)
            return self.add(name, content, True)
        else:
            name = file_name or os.path.basename(path_or_file.name)
            content = path_or_file.read()
            return self.add(name, content, True)

    def upload_file(
        self,
        path_or_file: Union[str, "os.PathLike[str]", IO],
        file_name: Optional[str] = None,
        *,
        chunk_size: int = _DEFAULT_CHUNK_SIZE,
        progress: Optional[ProgressCallback] = None,
    ) -> File:
        """Uploads a local file or stream, dispatching by size.

        The filesystem counterpart of :meth:`upload_content` (which takes
        ``bytes``): files at or below ``chunk_size`` go up in a single request,
        larger ones use a resumable :meth:`create_upload_session`. A
        ``str``/``os.PathLike`` source is opened and closed here; an already-open
        stream is read in place and left for the caller. The returned
        :class:`File` is deferred — the caller executes it.

        Args:
            path_or_file (str or os.PathLike or typing.IO): Path of the file to
                upload, or an open binary stream.
            file_name (str): Name to store the file under; defaults to the source
                base name (required for an unnamed stream).
            chunk_size (int): Simple-upload threshold / session chunk size (bytes).
            progress: Optional hook invoked with a ``Progress`` snapshot
              (``done``/``total`` in bytes; per chunk for session uploads, once
              after the upload completes for the simple path).
        """
        if isinstance(path_or_file, (str, os.PathLike)):
            path = os.fspath(path_or_file)
            name = file_name or os.path.basename(path)
            if os.path.getsize(path) > chunk_size:
                return self.create_upload_session(path, chunk_size=chunk_size, file_name=name, progress=progress)
            with open(path, "rb") as f:
                return self._simple_upload(name, f.read(), progress)
        stream = path_or_file
        size = _stream_size(stream)
        if not file_name:
            stream_name = getattr(stream, "name", None)
            file_name = os.path.basename(stream_name) if stream_name else None
        if not file_name:
            raise ValueError("file_name is required when uploading from an unnamed stream")
        if size > chunk_size:
            return self.create_upload_session(stream, chunk_size=chunk_size, file_name=file_name, progress=progress)
        return self._simple_upload(file_name, stream.read(), progress)

    def _simple_upload(
        self, file_name: str, content: Optional[bytes], progress: Optional[ProgressCallback] = None
    ) -> File:
        """Queue a single-request ``Files/add`` upload with an optional progress hook."""
        file = self.add(file_name, content, True)
        if callable(progress):
            size = len(content) if content else 0

            def _uploaded(_: Any) -> None:
                progress(Progress(done=size, total=size, stage="uploading"))

            file.after_execute(_uploaded)
        return file

    @limit(Limits.FILE_UPLOAD)
    def upload_content(
        self,
        content: bytes,
        file_name: str,
        chunk_size: int = _DEFAULT_CHUNK_SIZE,
        progress: Optional[ProgressCallback] = None,
    ) -> File:
        """Uploads in-memory content, dispatching by size.

        Files at or below ``chunk_size`` use the simple :meth:`upload`; larger
        ones use a resumable :meth:`create_upload_session` (staged to a temp
        file). The returned :class:`File` is deferred — the caller executes it.

        Args:
            content (bytes): File content to upload.
            file_name (str): New file name.
            chunk_size (int): Upload-session chunk size / size threshold (bytes).
            progress: Optional hook invoked with a ``Progress`` snapshot
              (``done``/``total`` in bytes; per chunk for session uploads, once
              after the upload completes for the simple path).
        """
        ensure_within(Limits.FILE_UPLOAD, len(content), context=f"file '{file_name}'")
        if len(content) <= chunk_size:
            return self._simple_upload(file_name, content, progress)
        with tempfile.NamedTemporaryFile(suffix=file_name) as tmp:
            tmp.write(content)
            tmp.flush()
            return self.create_upload_session(tmp.name, chunk_size=chunk_size, file_name=file_name, progress=progress)

    def upload_with_checksum(self, file_object: IO, chunk_size: int = 1024) -> File:
        """ """
        h = hashlib.md5()
        file_name = os.path.basename(file_object.name)
        upload_id = str(uuid.uuid4())

        def _upload_session(return_type: File) -> None:
            content = file_object.read(chunk_size)
            h.update(content)

            return_type.upload_with_checksum(upload_id, h.hexdigest(), content)

        return self.add(file_name, None, True).after_execute(_upload_session)

    def _build_upload_session_query(
        self,
        return_type: File,
        file_name: str,
        stream: IO,
        file_size: int,
        chunk_size: int,
        chunk_uploaded: Optional[Callable[[int, Any], None]] = None,
        progress: Optional[ProgressCallback] = None,
        close_on_finish: bool = False,
        **kwargs: Any,
    ) -> ServiceOperationQuery:
        """Build (but do not queue) a resumable upload chain for ``return_type``.

        Returns the first query (the ``Files/add`` placeholder); once it runs, the
        attached ``_upload`` handler reads and sends each fragment through
        ``startUpload``/``continueUpload``/``finishUpload``. The chain is bound to
        the placeholder query by id rather than to the last queued query, so it
        also fires when ``ensure_file`` defers the placeholder into the create
        slot of ``get_or_create``.
        """
        upload_id = str(uuid.uuid4())
        first = self._build_upload_query(return_type, file_name, None, True)

        def _upload(_: Any) -> None:
            uploaded_bytes = stream.tell()
            if callable(chunk_uploaded):
                chunk_uploaded(uploaded_bytes, **kwargs)  # type: ignore[call-arg]
            if callable(progress):
                progress(Progress(done=uploaded_bytes, total=file_size, stage="uploading"))

            content = stream.read(chunk_size)
            if uploaded_bytes == file_size:
                if close_on_finish and not stream.closed:
                    stream.close()
                return

            if uploaded_bytes == 0:
                result = return_type.start_upload(upload_id, content)
            elif uploaded_bytes + len(content) < file_size:
                result = return_type.continue_upload(upload_id, uploaded_bytes, content)
            else:
                result = return_type.finish_upload(upload_id, uploaded_bytes, content)
            result.after_execute(_upload)

        context = self.context
        context.pending_request().after_execute(
            _upload,
            once=True,
            condition=lambda: context.current_query is not None and context.current_query.id == first.id,
        )
        return first

    def create_upload_session(
        self,
        file_or_path: IO | str,
        chunk_size: int,
        chunk_uploaded: Optional[Callable[[int, Any], None]] = None,
        progress: Optional[ProgressCallback] = None,
        file_name: Optional[str] = None,
        **kwargs: Any,
    ) -> File:
        """
        Creates an upload session with progress callback support.

        Args:
            file_or_path: File object or path to upload
            chunk_size: Size of upload chunks in bytes
            chunk_uploaded: Callback that accepts offset and optional additional args
            progress: Optional hook invoked per uploaded chunk with a
              ``Progress`` snapshot (``done`` = bytes uploaded, ``total`` = file size).
            file_name: Optional name for the uploaded file
            **kwargs: Additional arguments passed to the upload implementation
        """
        auto_close = False
        if isinstance(file_or_path, (str, os.PathLike)):
            f: IO = open(file_or_path, "rb")
            auto_close = True
        else:
            f = file_or_path

        file_size = _stream_size(f)
        if file_name is None:
            stream_name = getattr(f, "name", None)
            file_name = os.path.basename(stream_name) if stream_name else None
        if not file_name:
            raise ValueError("file_name is required when uploading from an unnamed stream")

        return_type = File(self.context)
        if file_size > chunk_size:
            query = self._build_upload_session_query(
                return_type,
                file_name,
                f,
                file_size,
                chunk_size,
                chunk_uploaded=chunk_uploaded,
                progress=progress,
                close_on_finish=auto_close,
                **kwargs,
            )
        else:
            query = self._build_upload_query(return_type, file_name, f.read(), True)
            if auto_close and not f.closed:
                f.close()
        self.context.add_query(query)
        return return_type

    async def create_upload_session_async(
        self,
        file_or_path: IO | str,
        chunk_size: int,
        chunk_uploaded: Optional[Callable[[int, Any], None]] = None,
        progress: Optional[ProgressCallback] = None,
        file_name: Optional[str] = None,
        **kwargs: Any,
    ) -> File:
        """Awaitable twin of :meth:`create_upload_session` that never blocks the loop.

        Unlike the deferred synchronous form, this is an awaitable coroutine: it
        creates the file, uploads every chunk and commits the last fragment before
        it returns. Each chunk is read from the source stream on the shared
        offload executor and sent through the context's async transport (native
        with ``httpx``, otherwise a worker thread), so a large upload keeps the
        event loop free. ``chunk_uploaded`` and ``progress`` behave exactly as on
        the synchronous twin: invoked with the offset of the chunk about to be
        sent, then once more with the full size once every range is committed.

        Args:
            file_or_path: File object or path to upload.
            chunk_size: Size of upload chunks in bytes.
            chunk_uploaded: Callback that accepts the current offset and any extra
                keyword arguments.
            progress: Optional hook invoked per chunk with a ``Progress`` snapshot
                (``done`` = bytes uploaded, ``total`` = file size).
            file_name: Optional name for the uploaded file.
            **kwargs: Additional arguments passed through to ``chunk_uploaded``.

        Returns:
            File: The uploaded file.
        """
        executor = get_offload_executor()

        auto_close = False
        if isinstance(file_or_path, str):
            f: IO[bytes] = await run_offloaded(open, file_or_path, "rb", executor=executor)
            auto_close = True
        else:
            f = file_or_path

        file_size = _stream_size(f)
        if file_name is None:
            stream_name = getattr(f, "name", None)
            file_name = os.path.basename(stream_name) if stream_name else None
        if not file_name:
            raise ValueError("file_name is required when uploading from an unnamed stream")
        upload_id = str(uuid.uuid4())

        try:
            if file_size <= chunk_size:
                return_type = self.add(file_name, await run_offloaded(f.read, executor=executor), True)
                await self.context.execute_query_async()
                return return_type

            return_type = self.add(file_name, None, True)
            await self.context.execute_query_async()

            uploaded_bytes = 0
            while uploaded_bytes < file_size:
                if callable(chunk_uploaded):
                    chunk_uploaded(uploaded_bytes, **kwargs)  # type: ignore[call-arg]
                if callable(progress):
                    progress(Progress(done=uploaded_bytes, total=file_size, stage="uploading"))

                content = await run_offloaded(f.read, chunk_size, executor=executor)
                if uploaded_bytes == 0:
                    return_type.start_upload(upload_id, content)
                elif uploaded_bytes + len(content) < file_size:
                    return_type.continue_upload(upload_id, uploaded_bytes, content)
                else:
                    return_type.finish_upload(upload_id, uploaded_bytes, content)
                await self.context.execute_query_async()
                uploaded_bytes += len(content)

            if callable(chunk_uploaded):
                chunk_uploaded(file_size, **kwargs)  # type: ignore[call-arg]
            if callable(progress):
                progress(Progress(done=file_size, total=file_size, stage="uploading"))
            return return_type
        finally:
            if auto_close and not f.closed:
                f.close()

    def _build_upload_query(
        self,
        return_type: File,
        url: str,
        content: Optional[bytes | str] = None,
        overwrite: bool = False,
    ) -> ServiceOperationQuery:
        """Build (but do not queue) the simple ``Files/add`` upload query for ``return_type``.

        Shared by :meth:`add` and :meth:`Folder.ensure_file` — the latter needs a
        query it can hand to ``get_or_create``'s deferred create slot, bound to a
        file it can address afterwards.
        """
        self.add_child(return_type)
        params = FileCreationInformation(Url=url, Overwrite=overwrite)
        return ServiceOperationQuery(self, "add", params.to_json(), content, None, return_type)  # type: ignore[arg-type]

    def add(self, url: str, content: Optional[bytes | str] = None, overwrite=False) -> File:
        """Adds a file to the collection based on provided file creation information. A reference to the SP.File that
        was added is returned.

        Args:
            url (str): Specifies the URL of the file to be added. It MUST NOT be NULL.
                It MUST be a URL of relative or absolute form. Its length MUST be equal to or greater than 1.
            overwrite (bool): Specifies whether to overwrite an existing file with the same name and in the same
                location as the one being added.
            content (str or bytes or None): Specifies the binary content of the file to be added.
        """
        return_type = File(self.context)
        self.context.add_query(self._build_upload_query(return_type, url, content, overwrite))
        return return_type

    def add_template_file(self, url_of_file: str, template_file_type: TemplateFileType):
        """Adds a ghosted file to an existing list or document library.

        Args:
            url_of_file (str): server relative url of a file
            template_file_type (int): refer TemplateFileType enum
        """
        return_type = File(self.context)
        self.add_child(return_type)

        def _add_template_file():
            params = {
                "urlOfFile": str(SPResPath.create_relative(self.parent.properties["ServerRelativeUrl"], url_of_file)),
                "templateFileType": template_file_type.value,
            }
            qry = ServiceOperationQuery(self, "addTemplateFile", params, None, None, return_type)
            self.context.add_query(qry)

        self.parent.ensure_property("ServerRelativeUrl").after_execute(lambda _: _add_template_file())
        return return_type

    def download(
        self,
        target_dir: Union[str, "Path"],
        *,
        overwrite: bool = False,
        resume: bool = False,
        progress: Optional[ProgressCallback] = None,
    ) -> "DownloadOperation":
        """Download this collection's files into a local directory, concurrently.

        Uses the already-loaded items; if the collection was not loaded, it is
        enumerated first (paged). Files are written flat into ``target_dir``.
        Returns a deferred
        :class:`~office365.sharepoint.files.download_operation.DownloadOperation`;
        drive it with ``execute_query()`` or ``await execute_query_async()``.

        Args:
            target_dir: Local directory to write files into (created as needed).
            overwrite: When ``False`` (default) existing files are skipped, so a
              re-run resumes where it left off.
            resume: When ``True``, an existing but incomplete destination is
              completed by fetching only the missing byte range, instead of
              being skipped.
            progress: Optional hook invoked with ``Progress`` snapshots
              (``stage="scanning"`` while enumerating, ``"downloading"`` while
              transferring).

        Returns:
            A deferred bulk-download operation.
        """
        from office365.sharepoint.files.download_operation import DownloadOperation

        return DownloadOperation.for_collection(self, target_dir, overwrite=overwrite, resume=resume, progress=progress)

    def get_by_url(self, url: str) -> File:
        """Retrieve File object by url"""
        return File(self.context, ServiceOperationPath("GetByUrl", [url], self.resource_path))

    def get_by_id(self, id_: int) -> File:
        """Gets the File with the specified ID."""
        return File(self.context, ServiceOperationPath("getById", [id_], self.resource_path))

    @property
    def parent(self) -> Folder:
        """ """
        from office365.sharepoint.folders.folder import Folder

        return cast(Folder, self._parent)
