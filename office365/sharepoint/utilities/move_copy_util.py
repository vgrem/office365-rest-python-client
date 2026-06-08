from __future__ import annotations

import os
from typing import IO, TYPE_CHECKING, AnyStr, Callable, Optional

from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath

if TYPE_CHECKING:
    from office365.sharepoint.files.file import File
    from office365.sharepoint.folders.folder import Folder


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
    ) -> Folder:
        """Downloads a folder into a zip file

        Args:
            remove_folder (office365.sharepoint.folders.folder.Folder): Parent folder
            download_file (typing.IO): A download zip file object
            after_file_downloaded ((office365.sharepoint.files.file.File)->None): A download callback
            recursive (bool): Determines whether to traverse folders recursively
        """
        import zipfile

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

        def _download_file(file: File) -> None:
            def _after_downloaded(result: ClientResult[AnyStr]) -> None:
                filename = _get_relative_file_path(file)
                if callable(after_file_downloaded):
                    after_file_downloaded(file)
                with zipfile.ZipFile(download_file.name, "a", zipfile.ZIP_DEFLATED) as zf:
                    zf.writestr(filename, result.value)

            file.get_content().after_execute(_after_downloaded)

        def _download_folder(folder: Folder) -> None:
            def _download_files(rt):
                [_download_file(file) for file in folder.files]
                if recursive:
                    [_download_folder(sub_folder) for sub_folder in folder.folders]

            folder.expand(["Files", "Folders"]).get().after_execute(_download_files)

        _download_folder(remove_folder)
        return remove_folder
