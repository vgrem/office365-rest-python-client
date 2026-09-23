"""SharePoint Migration API package — manifest XML models + a package builder.

Assembles the XML manifest documents and content blobs ingested by the server-side
Migration API (``Site.create_migration_job`` / ``create_migration_job_encrypted``).
Covers the **document-library subset** (webs, lists, folders, files, versions).
"""

from __future__ import annotations

from office365.migration.package.builder import DEFAULT_NAMESPACE, Package, PackageBuilder
from office365.migration.package.manifest_xml import (
    EXPORT_SETTINGS_NS,
    LOOKUP_LIST_MAP_NS,
    MANIFEST_NS,
    REQUIREMENTS_NS,
    ROOT_OBJECT_MAP_NS,
    SOURCE_TYPES,
    SYSTEM_DATA_NS,
    USER_GROUP_MAP_NS,
    VIEW_FORMS_LIST_NS,
    DeploymentObject,
    ExportSettings,
    Group,
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
from office365.migration.package.staging import (
    AzureBlobStaging,
    BlobStaging,
    FileSystemStaging,
    Staging,
    create_staging,
)

__all__ = [
    "DEFAULT_NAMESPACE",
    "EXPORT_SETTINGS_NS",
    "LOOKUP_LIST_MAP_NS",
    "MANIFEST_NS",
    "REQUIREMENTS_NS",
    "ROOT_OBJECT_MAP_NS",
    "SOURCE_TYPES",
    "SYSTEM_DATA_NS",
    "USER_GROUP_MAP_NS",
    "VIEW_FORMS_LIST_NS",
    "AzureBlobStaging",
    "BlobStaging",
    "DeploymentObject",
    "ExportSettings",
    "FileSystemStaging",
    "Group",
    "Manifest",
    "ManifestObject",
    "Package",
    "PackageBuilder",
    "RootObject",
    "RootObjectMap",
    "Staging",
    "SystemData",
    "SystemObject",
    "User",
    "UserGroupMap",
    "create_staging",
    "empty_document",
]
