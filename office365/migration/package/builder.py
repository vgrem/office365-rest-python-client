"""Package builder — assemble a SharePoint Migration API package.

Walks a document library's files and folders into the manifest XML documents
(``Manifest.xml`` / ``ExportSettings.xml`` / ``SystemData.xml`` / ``UserGroup.xml``)
plus the content blobs, ready to stage in Azure Storage and submit via
``Site.create_migration_job`` / ``create_migration_job_encrypted``.

The ``Manifest.xml`` shape follows the working ``MigrationApiDemo`` sample: a
library root ``SPFolder``, the ``SPDocumentLibrary``, then an ``SPFolder`` per
subfolder and an ``SPFile`` per file (no ``SPWeb``/``SPList`` objects — those are
the target system objects). Content blobs are named after the file's GUID and
referenced from ``<File FileValue="…">``; older versions get a ``<guid>.<version>``
blob. IDs are **deterministic** (``uuid5`` of the item path), so rebuilding the
same content yields the same package.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from office365.migration.package.manifest_xml import (
    LOOKUP_LIST_MAP_NS,
    REQUIREMENTS_NS,
    VIEW_FORMS_LIST_NS,
    DeploymentObject,
    ExportSettings,
    Manifest,
    ManifestObject,
    RootObject,
    RootObjectMap,
    SystemData,
    SystemObject,
    User,
    UserGroupMap,
    empty_document,
)

# Stable namespace so item GUIDs are reproducible across runs.
DEFAULT_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, "office365-rest-python-client/migration")

# ``SPListTemplateType`` for a document library (a free string in the schema).
_DOCUMENT_LIBRARY_TEMPLATE = "DocumentLibrary"

__all__ = ["DEFAULT_NAMESPACE", "Package", "PackageBuilder"]


def _normalize(path: str) -> str:
    """Normalize a library-relative path (no leading/trailing slash, ``/`` separators)."""
    return path.replace("\\", "/").strip("/")


@dataclass
class Package:
    """An assembled migration package: manifest documents + content blobs.

    ``Requirements.xml`` / ``RootObjectMap.xml`` / ``LookupListMap.xml`` /
    ``ViewFormsList.xml`` are documented as optional, but the ingestion service
    fetches them by name — a missing one fails the job with a 404.
    """

    manifest: bytes
    export_settings: bytes
    system_data: bytes
    user_group_map: bytes
    requirements: bytes = b""
    root_object_map: bytes = b""
    lookup_list_map: bytes = b""
    view_forms_list: bytes = b""
    content: dict[str, bytes] = field(default_factory=dict)

    def blobs(self) -> dict[str, bytes]:
        """The manifest-package blobs by file name (go to the manifest container)."""
        return {
            "Manifest.xml": self.manifest,
            "ExportSettings.xml": self.export_settings,
            "SystemData.xml": self.system_data,
            "UserGroup.xml": self.user_group_map,
            "Requirements.xml": self.requirements,
            "RootObjectMap.xml": self.root_object_map,
            "LookupListMap.xml": self.lookup_list_map,
            "ViewFormsList.xml": self.view_forms_list,
        }

    def save(self, directory: str | Path) -> list[Path]:
        """Write the manifest files and content blobs under ``directory``.

        Layout: ``<directory>/manifest/<Name>.xml`` and
        ``<directory>/content/<blob>`` — matching the two Azure containers.
        """
        root = Path(directory)
        (root / "manifest").mkdir(parents=True, exist_ok=True)
        (root / "content").mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        for name, data in self.blobs().items():
            path = root / "manifest" / name
            path.write_bytes(data)
            written.append(path)
        for name, data in self.content.items():
            path = root / "content" / name
            path.write_bytes(data)
            written.append(path)
        return written


class PackageBuilder:
    """Assembles a document-library migration package."""

    def __init__(
        self,
        site_url: str,
        *,
        web_id: str | None = None,
        web_url: str = "/",
        list_id: str | None = None,
        list_title: str = "Documents",
        list_url: str | None = None,
        root_folder_id: str | None = None,
        root_folder_parent_id: str | None = None,
        source_type: str = "SharePointOnline",
        include_security: str = "None",
        namespace: uuid.UUID | None = None,
    ) -> None:
        self._namespace = namespace or DEFAULT_NAMESPACE
        self._web_id = web_id or str(self._guid("web"))
        self._web_url = web_url
        self._list_id = list_id or str(self._guid("list"))
        self._list_title = list_title
        self._list_url = list_url or f"{web_url.rstrip('/')}/{list_title}"
        self._root_folder_id = root_folder_id or self._list_id
        self._root_folder_parent_id = root_folder_parent_id or self._web_id
        self._export = ExportSettings(
            site_url=site_url,
            source_type=source_type,
            include_security=include_security,
            export_objects=[DeploymentObject(id=self._list_id, type="List", parent_id=self._web_id)],
        )
        self._manifest = Manifest()
        self._user_group_map = UserGroupMap()
        self._content: dict[str, bytes] = {}
        self._folders: dict[str, str] = {}
        self._files: dict[str, str] = {}
        self._list_item_int_id = 0
        self._add_root()
        self._add_document_library()

    # ── Content ──────────────────────────────────────────────────

    def add_folder(
        self,
        path: str,
        *,
        time_created: str | None = None,
        time_last_modified: str | None = None,
    ) -> str:
        """Add a folder (and any missing parents); returns its GUID."""
        path = _normalize(path)
        if path in self._folders:
            return self._folders[path]
        parent_id = self._parent_id(path)
        folder_id = str(self._guid(f"folder:{path}"))
        self._manifest.add(
            ManifestObject(
                id=folder_id,
                object_type="SPFolder",
                element="Folder",
                attributes={
                    "Id": folder_id,
                    "Name": path,
                    "Url": self._url(path),
                    "ParentFolderId": parent_id,
                    "ParentWebId": self._web_id,
                    "ParentWebUrl": self._web_url,
                    "ContainingDocumentLibrary": self._list_id,
                    "TimeCreated": time_created,
                    "TimeLastModified": time_last_modified,
                },
                parent_id=parent_id,
                parent_web_id=self._web_id,
                parent_web_url=self._web_url,
                url=self._url(path),
            )
        )
        self._folders[path] = folder_id
        return folder_id

    def add_file(
        self,
        path: str,
        content: bytes,
        *,
        time_created: str | None = None,
        time_last_modified: str | None = None,
        version: str = "1.0",
        versions: list[tuple[str, bytes]] | None = None,
        list_item_int_id: int | None = None,
    ) -> str:
        """Add a file (and any missing parent folders); returns its GUID.

        Args:
            path: Library-relative path.
            content: The current version's bytes.
            version: The current version label (e.g. ``"1.0"``).
            versions: Older versions as ``(version, content)`` pairs.
            list_item_int_id: Optional list-item integer id to preserve.
        """
        path = _normalize(path)
        parent_id = self._parent_id(path)
        file_id = str(self._guid(f"file:{path}"))
        url = self._url(path)
        self._content[file_id] = content
        self._list_item_int_id += 1
        version_rows: list[dict] = []
        for older_version, older_content in versions or []:
            blob = f"{file_id}.{older_version}"
            self._content[blob] = older_content
            version_rows.append(
                {
                    "Id": file_id,
                    "Name": path,
                    "Url": url,
                    "ParentWebId": self._web_id,
                    "ParentWebUrl": self._web_url,
                    "ParentId": parent_id,
                    "ListId": self._list_id,
                    "FileValue": blob,
                    "Version": older_version,
                }
            )
        self._manifest.add(
            ManifestObject(
                id=file_id,
                object_type="SPFile",
                element="File",
                attributes={
                    "Id": file_id,
                    "Name": path,
                    "Url": url,
                    "ParentId": parent_id,
                    "ParentWebId": self._web_id,
                    "ParentWebUrl": self._web_url,
                    "ListId": self._list_id,
                    "FileValue": file_id,
                    "ListItemIntId": list_item_int_id or self._list_item_int_id,
                    "Version": version,
                    "TimeCreated": time_created,
                    "TimeLastModified": time_last_modified,
                },
                parent_id=parent_id,
                parent_web_id=self._web_id,
                parent_web_url=self._web_url,
                url=url,
                versions=version_rows,
            )
        )
        self._files[path] = file_id
        return file_id

    def add_user(
        self,
        login: str,
        *,
        name: str | None = None,
        email: str | None = None,
        system_id: str | None = None,
        is_site_admin: bool = False,
    ) -> int:
        """Register a user in ``UserGroup.xml``; returns its integer id."""
        user_id = len(self._user_group_map.users) + 1
        self._user_group_map.add_user(
            User(
                id=user_id,
                name=name or login,
                login=login,
                email=email,
                system_id=system_id,
                is_site_admin=is_site_admin,
            )
        )
        return user_id

    def build(self) -> Package:
        """Render the manifest documents and freeze the content blobs."""
        system_data = SystemData(
            system_objects=[
                SystemObject(id=self._web_id, type="Web", url=self._web_url),
                SystemObject(id=self._list_id, type="List", url=self._list_url),
            ]
        )
        root_object_map = RootObjectMap(
            objects=[
                RootObject(
                    id=self._list_id,
                    type="List",
                    parent_id=self._web_id,
                    web_url=self._web_url,
                    url=self._list_url,
                )
            ]
        )
        return Package(
            manifest=self._manifest.to_xml(),
            export_settings=self._export.to_xml(),
            system_data=system_data.to_xml(),
            user_group_map=self._user_group_map.to_xml(),
            requirements=empty_document(REQUIREMENTS_NS, "Requirements"),
            root_object_map=root_object_map.to_xml(),
            lookup_list_map=empty_document(LOOKUP_LIST_MAP_NS, "LookupLists"),
            view_forms_list=empty_document(VIEW_FORMS_LIST_NS, "ViewFormsList"),
            content=dict(self._content),
        )

    # ── Manifest objects ─────────────────────────────────────────

    def _add_root(self) -> None:
        """The library root folder (``SPFolder``) — the package's entry point."""
        self._manifest.add(
            ManifestObject(
                id=self._root_folder_id,
                object_type="SPFolder",
                element="Folder",
                attributes={
                    "Id": self._root_folder_id,
                    "Name": self._list_name,
                    "Url": self._list_name,
                    "ParentFolderId": self._root_folder_parent_id,
                    "ParentWebId": self._web_id,
                    "ParentWebUrl": self._web_url,
                    "ContainingDocumentLibrary": self._list_id,
                },
                parent_id=self._root_folder_parent_id,
                parent_web_id=self._web_id,
                parent_web_url=self._web_url,
                url=self._list_url,
            )
        )

    def _add_document_library(self) -> None:
        """The target document library (``SPDocumentLibrary``)."""
        self._manifest.add(
            ManifestObject(
                id=self._list_id,
                object_type="SPDocumentLibrary",
                element="DocumentLibrary",
                attributes={
                    "Id": self._list_id,
                    "BaseTemplate": _DOCUMENT_LIBRARY_TEMPLATE,
                    "ParentWebId": self._web_id,
                    "ParentWebUrl": self._web_url,
                    "RootFolderId": self._root_folder_id,
                    "RootFolderUrl": self._list_url,
                    "Title": self._list_title,
                },
                parent_id=self._web_id,
                parent_web_id=self._web_id,
                parent_web_url=self._web_url,
                url=self._list_url,
            )
        )

    # ── Helpers ──────────────────────────────────────────────────

    @property
    def _list_name(self) -> str:
        return self._list_url.rstrip("/").rsplit("/", 1)[-1]

    def _guid(self, key: str) -> uuid.UUID:
        return uuid.uuid5(self._namespace, key)

    def _url(self, path: str) -> str:
        """The website-relative URL of an item (no leading slash, per the schema)."""
        return f"{self._list_url.strip('/')}/{path}"

    def _parent_id(self, path: str) -> str:
        """The parent folder's GUID (the library root when top-level)."""
        parent = PurePosixPath(path).parent
        if str(parent) in (".", ""):
            return self._root_folder_id
        return self.add_folder(str(parent))
