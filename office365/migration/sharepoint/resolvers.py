"""Resolve a declarative :class:`MigrationTask` into source/target adapters.

SPMT-shaped tasks (``Add-SPMTTask``) name a source and a target site/list; this
turns them into the toolkit's ``DataSource``/``DataTarget`` pair against a
SharePoint ``ClientContext``. Client-side REST uploads are the default; set
``MigrationSettings.use_migration_api`` for the server-side Migration API path
(full fidelity: versions/ACLs).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from office365.migration.adapters.filesystem import FileSystemSource
from office365.migration.tasks import FILE_SHARE, SHAREPOINT, MigrationTask

if TYPE_CHECKING:
    from office365.migration.settings import MigrationSettings

__all__ = ["resolve_task"]


def resolve_task(task: MigrationTask, context, settings: "MigrationSettings | None" = None):
    """Return a ``(source, target)`` adapter pair for a task descriptor."""
    if task.kind == FILE_SHARE:
        return _file_share(task, context, settings)
    if task.kind == SHAREPOINT:
        return _sharepoint(task, context, settings)
    raise ValueError(f"unsupported task kind {task.kind!r}")


def _file_share(task: MigrationTask, context, settings):
    if not task.file_share_source:
        raise ValueError("a file-share task requires file_share_source")
    source = FileSystemSource(task.file_share_source)
    library, folder = _target_folder(context, task)
    return source, _build_target(task, context, settings, library, folder)


def _sharepoint(task: MigrationTask, context, settings):
    from office365.migration.sharepoint.adapters import SharePointLibrarySource

    if task.migrate_all or not task.source_list:
        raise NotImplementedError(
            "SharePoint-source tasks need a source list; migrate-all / whole-site migrations are not supported yet"
        )
    source_list = context.web.get_list_by_title(task.source_list)
    source = SharePointLibrarySource(source_list.root_folder)
    library, folder = _target_folder(context, task)
    return source, _build_target(task, context, settings, library, folder)


def _target_folder(context, task: MigrationTask):
    """The target library (and, when set, its relative subfolder)."""
    library = context.web.get_list_by_title(task.target_list).get().execute_query()
    folder = library.root_folder.get().execute_query()
    if task.target_list_relative_path:
        url = f"{(folder.server_relative_url or '').rstrip('/')}/{task.target_list_relative_path.strip('/')}"
        folder = context.web.get_folder_by_server_relative_url(url)
    return library, folder


def _build_target(task: MigrationTask, context, settings, library, folder):
    if settings is not None and settings.use_migration_api:
        return _package_target(task, context, library)
    from office365.migration.sharepoint.adapters import SharePointLibraryTarget

    return SharePointLibraryTarget(folder)


def _package_target(task: MigrationTask, context, library):
    """The server-side Migration API target (provisions containers)."""
    from urllib.parse import urlparse

    from office365.migration.sharepoint.package_target import SharePointPackageTarget

    web = context.web.get().execute_query()
    root = library.root_folder
    root.ensure_properties(["UniqueId", "ServerRelativeUrl"]).execute_query()
    parent = root.parent_folder.ensure_property("UniqueId")
    parent.execute_query()
    containers = context.site.provision_migration_containers().execute_query().value
    return SharePointPackageTarget(
        context.site,
        web.id,
        content_uri=containers.DataContainerUri,
        manifest_uri=containers.MetadataContainerUri,
        encryption_key=containers.EncryptionKey,
        site_url=context.base_url,
        list_title=library.title,
        list_url=root.server_relative_url,
        web_url=urlparse(context.base_url).path or "/",
        root_folder_id=root.unique_id,
        root_folder_parent_id=parent.unique_id,
        source_type="FileShare" if task.kind == FILE_SHARE else "SharePointOnline",
    )
