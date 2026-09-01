from __future__ import annotations

import os
from pathlib import Path
from typing import IO, TYPE_CHECKING, AnyStr, Callable, Iterable, Optional, Tuple, Union, cast

from office365.runtime.client_result import ClientResult
from office365.runtime.operations import Progress, ProgressCallback
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath

if TYPE_CHECKING:
    from office365.sharepoint.files.file import File
    from office365.sharepoint.folders.folder import Folder

_DEFAULT_CHUNK_SIZE = 4 * 1024 * 1024  # simple-upload threshold / upload-session chunk

UploadSource = Union[
    str,
    Path,
    Iterable[Union[str, Path, Tuple[str, Union[str, Path, bytes]]]],
]


class MoveCopyUtil(Entity):
    """A container class for static move/copy methods."""

    @staticmethod
    def copy_file_by_path(context, src_path, dest_path, overwrite, options=None):
        """Copies a file from a source URL to a destination URL.

        Args:
            context (office365.sharepoint.client_context.ClientContext): client context
            src_path (str): A full or server relative path that represents the source file.
            dest_path (str): A full or server relative url that represents the destination file.
            overwrite (bool): Overwrites the destination file when it exists.
            options (office365.sharepoint.utilities.move_copy_options.MoveCopyOptions or None):
        """
        return_type = ClientResult(context)
        payload = {
            "srcPath": SPResPath.create_absolute(context.base_url, src_path),
            "destPath": SPResPath.create_absolute(context.base_url, dest_path),
            "overwrite": overwrite,
            "options": options,
        }
        qry = ServiceOperationQuery(
            MoveCopyUtil(context),
            "CopyFileByPath",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def copy_folder(context, src_url, dest_url, options=None):
        """Copies a folder from a source URL to a destination URL.

        Args:
            context (office365.sharepoint.client_context.ClientContext): Client context
            src_url (str): A full or server relative url that represents the source folder.
            dest_url (str): A full or server relative url that represents the destination folder.
            options (office365.sharepoint.utilities.move_copy_options.MoveCopyOptions): Contains options used to
                modify the behavior.
        """
        return_type = ClientResult(context)
        binding_type = MoveCopyUtil(context)
        payload = {
            "srcUrl": str(SPResPath.create_absolute(context.base_url, src_url)),
            "destUrl": str(SPResPath.create_absolute(context.base_url, dest_url)),
            "options": options,
        }
        qry = ServiceOperationQuery(binding_type, "CopyFolder", None, payload, None, return_type, True)
        context.add_query(qry)
        return return_type

    @staticmethod
    def copy_folder_by_path(context, src_path, dest_path, options=None):
        """Copies a folder from a source URL to a destination URL.

        Args:
            context (office365.sharepoint.client_context.ClientContext): client context
            src_path (str): A full or server relative path that represents the source folder.
            dest_path (str): A full or server relative url that represents the destination folder.
            options (office365.sharepoint.utilities.move_copy_options.MoveCopyOptions or None):
        """
        return_type = ClientResult(context)
        payload = {
            "srcPath": SPResPath.create_absolute(context.base_url, src_path),
            "destPath": SPResPath.create_absolute(context.base_url, dest_path),
            "options": options,
        }
        qry = ServiceOperationQuery(
            MoveCopyUtil(context),
            "CopyFolderByPath",
            None,
            payload,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    def move_folder(context, src_url, dest_url, options):
        """Moves a folder from a source URL to a destination URL.

        Args:
            context (office365.sharepoint.client_context.ClientContext): client context
            src_url (str): A full or server relative url that represents the source folder.
            dest_url (str): A full or server relative url that represents the destination folder.
            options (office365.sharepoint.utilities.move_copy_options.MoveCopyOptions): Contains options used to
                modify the behavior.
        """
        binding_type = MoveCopyUtil(context)
        payload = {
            "srcUrl": str(SPResPath.create_absolute(context.base_url, src_url)),
            "destUrl": str(SPResPath.create_absolute(context.base_url, dest_url)),
            "options": options,
        }
        qry = ServiceOperationQuery(binding_type, "MoveFolder", None, payload, None, None, True)
        context.add_query(qry)
        return binding_type

    @staticmethod
    def move_folder_by_path(context, src_path, dest_path, options):
        """Moves a folder from a source URL to a destination URL.

        Args:
            src_path (str): A full or server relative path that represents the source folder.
            dest_path (str): A full or server relative path that represents the destination folder.
            context (office365.sharepoint.client_context.ClientContext): client context
            options (office365.sharepoint.utilities.move_copy_options.MoveCopyOptions): Contains options used to
                modify the behavior.
        """
        binding_type = MoveCopyUtil(context)
        payload = {
            "srcPath": SPResPath.create_absolute(context.base_url, src_path),
            "destPath": SPResPath.create_absolute(context.base_url, dest_path),
            "options": options,
        }
        qry = ServiceOperationQuery(binding_type, "MoveFolderByPath", None, payload, None, None, True)
        context.add_query(qry)
        return binding_type

    @staticmethod
    def download_folder(
        remove_folder: Folder,
        download_file: IO,
        after_file_downloaded: Optional[Callable[[File], None]] = None,
        recursive: bool = True,
        include_versions: bool = False,
        progress: Optional[ProgressCallback] = None,
    ) -> Folder:
        """Downloads a folder into a zip file

        Args:
            remove_folder (office365.sharepoint.folders.folder.Folder): Parent folder
            download_file (typing.IO): A download zip file object
            after_file_downloaded ((office365.sharepoint.files.file.File)->None): A download callback
            recursive (bool): Determines whether to traverse folders recursively
            include_versions (bool): If True, also downloads each file's version history
              into the zip under ``versions/{path}/v{label}``
            progress: Optional hook invoked per downloaded file with a
              ``Progress`` snapshot (total is unknown until the folder tree is
              walked).
        """
        import zipfile

        files_downloaded = 0

        def _get_relative_file_path(file: File) -> str:
            parent_folder = file.parent_folder
            assert parent_folder is not None
            assert parent_folder.server_relative_url is not None
            assert remove_folder.server_relative_url is not None
            assert file.name is not None
            return os.path.join(
                parent_folder.server_relative_url.replace(remove_folder.server_relative_url, ""),
                file.name,
            )

        def _download_versions(file: File, filename: str) -> None:
            def _versions_loaded(versions) -> None:
                for version in versions:
                    if version.is_current_version:
                        continue  # current content is saved at the zip root
                    label = (version.version_label or str(version.id)).replace(".", "_")

                    def _save(vresult: ClientResult[AnyStr], fn: str = filename, lbl: str = label) -> None:
                        with zipfile.ZipFile(download_file.name, "a", zipfile.ZIP_DEFLATED) as zf:
                            zf.writestr(f"versions/{fn}/v{lbl}", vresult.value)

                    version.open_binary_stream().after_execute(_save)

            file.versions.get().after_execute(_versions_loaded)

        def _download_file(file: File) -> None:
            def _after_downloaded(result: ClientResult[AnyStr]) -> None:
                nonlocal files_downloaded
                filename = _get_relative_file_path(file)
                if callable(after_file_downloaded):
                    after_file_downloaded(file)
                with zipfile.ZipFile(download_file.name, "a", zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr(filename, result.value)
                files_downloaded += 1
                if callable(progress):
                    progress(Progress(done=files_downloaded, stage="downloading"))
                if include_versions:
                    _download_versions(file, filename)

            file.get_content().after_execute(_after_downloaded)

        def _download_folder(folder: Folder) -> None:
            def _download_files(rt):
                [_download_file(file) for file in folder.files]
                if recursive:
                    [_download_folder(sub_folder) for sub_folder in folder.folders]

            folder.expand(["Files", "Folders"]).get().after_execute(_download_files)

        _download_folder(remove_folder)
        return remove_folder

    @staticmethod
    def upload_folder(
        target_folder: Folder,
        source: UploadSource,
        after_file_uploaded: Optional[Callable[[File], None]] = None,
        recursive: bool = True,
        progress: Optional[ProgressCallback] = None,
        chunk_size: int = _DEFAULT_CHUNK_SIZE,
    ) -> Folder:
        """Upload a local directory / files into a folder tree — sequential, deferred.

        The counterpart of :meth:`download_folder`: ``source`` may be

        - a **directory** ``str``/``Path`` (walked recursively, files uploaded
          at their relative path),
        - a **file** ``str``/``Path`` (uploaded at its file name),
        - an **iterable of file paths** (each uploaded at its file name), or
        - an **iterable of ``(relative_path, content)``** pairs where content is
          ``bytes`` (as-is), ``str`` (text, utf-8), or a ``Path`` (read lazily).

        Uploads run sequentially via a deferred ``after_execute`` chain — content
        is read lazily per file, and the caller's single ``execute_query()``
        drives the whole chain (bounded memory).

        Args:
            target_folder (office365.sharepoint.folders.folder.Folder): Target folder.
            source: Local directory / file / file list / (path, content) pairs.
            after_file_uploaded ((office365.sharepoint.files.file.File)->None): Per-file callback.
            recursive (bool): Traverse subdirectories when ``source`` is a directory.
            progress: Optional hook invoked per uploaded file with a ``Progress`` snapshot.
            chunk_size (int): Upload-session chunk size / size threshold (bytes).

        Returns:
            The target folder (chainable).
        """
        entries = MoveCopyUtil._collect_upload_entries(source, recursive)
        state = {"index": 0, "done": 0}
        total = len(entries)

        def _upload_next() -> None:
            if state["index"] >= total:
                return
            relative_path, provider = entries[state["index"]]
            state["index"] += 1

            def _after(file, rel=relative_path) -> None:
                state["done"] += 1
                if callable(after_file_uploaded):
                    after_file_uploaded(file)
                if callable(progress):
                    progress(Progress(done=state["done"], total=total, stage="uploading"))
                _upload_next()

            target_folder.upload_file(relative_path, provider(), chunk_size).after_execute(_after)

        if total:
            _upload_next()
        return target_folder

    @staticmethod
    def _collect_upload_entries(source: UploadSource, recursive: bool):
        """Normalize ``source`` into ``[(relative_path, lazy_content_provider)]``."""
        entries = []

        def _path_provider(path: Path) -> Callable[[], bytes]:
            return lambda: path.read_bytes()

        if isinstance(source, (str, Path)):
            path = Path(source)
            if path.is_dir():
                items = path.rglob("*") if recursive else path.iterdir()
                for item in sorted(items):
                    if item.is_file():
                        entries.append((item.relative_to(path).as_posix(), _path_provider(item)))
            elif path.is_file():
                entries.append((path.name, _path_provider(path)))
            return entries

        items = list(source)
        if not items:
            return entries
        first = items[0]
        if isinstance(first, tuple):  # noqa: PLR2004 — (path, content) pairs
            pairs = cast("list[Tuple[str, Union[str, Path, bytes]]]", items)
            for relative_path, content in pairs:
                entries.append((relative_path, _content_provider(content)))
        else:
            paths = cast("list[Union[str, Path]]", items)
            for item in paths:
                path = Path(item)
                entries.append((path.name, _path_provider(path)))
        return entries


def _content_provider(content):
    """Return a lazy bytes provider for ``(relative_path, content)`` values.

    ``bytes`` is used as-is, ``Path`` is read from disk lazily, and ``str`` is
    treated as text content (utf-8) — pass a ``Path`` when you mean a local file.
    """
    if isinstance(content, bytes):
        return lambda: content
    if isinstance(content, Path):
        return lambda: content.read_bytes()
    return lambda: str(content).encode("utf-8")
