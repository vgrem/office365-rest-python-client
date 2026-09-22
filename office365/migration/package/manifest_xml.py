"""SPO Migration API manifest package — XML models and serialization.

The SharePoint Migration API (``CreateMigrationJob`` /
``CreateMigrationJobEncrypted``) ingests content described by a set of XML
manifest files. This module models the **document-library subset** — webs, lists,
folders, files, and file versions — plus the small, fully-specified
``ExportSettings.xml`` / ``SystemData.xml`` / ``UserGroupMap.xml``.

The full ``DeploymentManifest`` schema has 100+ elements (content types, views,
web parts, list items, taxonomy, ...); only what a document-library migration
needs is modeled here. The generated XML follows the documented format but is
**not yet verified against a live tenant**.

References:
- https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-manifest
- https://learn.microsoft.com/en-us/sharepoint/dev/schema/deploymentmanifest-schema
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

MANIFEST_NS = "urn:deployment-manifest-schema"
SYSTEM_DATA_NS = "urn:deployment-systemdata-schema"
EXPORT_SETTINGS_NS = "urn:deployment-exportsettings-schema"
USER_GROUP_MAP_NS = "urn:deployment-usergroupmap-schema"

# ``ExportSettings/@SourceType`` accepted values.
SOURCE_TYPES = (
    "AmazonS3",
    "AzureStorage",
    "Box",
    "Dropbox",
    "Egnyte",
    "FileShare",
    "GoogleCloudStorage",
    "GoogleDrive",
    "MicrosoftStream",
    "OneDrive",
    "SharePointOnline",
    "SharePointOnPremServer",
    "Other",
)

__all__ = [
    "EXPORT_SETTINGS_NS",
    "MANIFEST_NS",
    "SOURCE_TYPES",
    "SYSTEM_DATA_NS",
    "USER_GROUP_MAP_NS",
    "DeploymentObject",
    "ExportSettings",
    "Group",
    "Manifest",
    "ManifestObject",
    "SystemData",
    "SystemObject",
    "User",
    "UserGroupMap",
]


def _q(ns: str, tag: str) -> str:
    """Qualify a tag with its XML namespace."""
    return f"{{{ns}}}{tag}"


def _str(value: object) -> str:
    """Render an attribute value (booleans as lowercase ``true``/``false``)."""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _set(element: ET.Element, attributes: dict) -> None:
    """Set non-``None`` attributes on an element, in insertion order."""
    for name, value in attributes.items():
        if value is not None:
            element.set(name, _str(value))


def _serialize(root: ET.Element, ns: str) -> bytes:
    """Serialize a document with ``ns`` as the default namespace + XML declaration."""
    ET.register_namespace("", ns)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


@dataclass
class ManifestObject:
    """A single ``<SPObject>`` entry in ``Manifest.xml``.

    ``attributes`` are rendered on the child element (``element``); ``versions``
    are rendered as a nested ``<Versions><File .../></Versions>`` block.
    """

    id: str
    object_type: str  # Web | List | Folder | File
    element: str  # child element name (Web/List/Folder/File)
    attributes: dict = field(default_factory=dict)
    parent_id: str | None = None
    parent_web_id: str | None = None
    parent_web_url: str | None = None
    versions: list[dict] = field(default_factory=list)


@dataclass
class Manifest:
    """The ``Manifest.xml`` document — the content/structure catalog."""

    objects: list[ManifestObject] = field(default_factory=list)

    def add(self, obj: ManifestObject) -> "Manifest":
        self.objects.append(obj)
        return self

    def to_xml(self) -> bytes:
        root = ET.Element(_q(MANIFEST_NS, "SPObjects"))
        for obj in self.objects:
            sp = ET.SubElement(root, _q(MANIFEST_NS, "SPObject"))
            _set(
                sp,
                {
                    "Id": obj.id,
                    "ObjectType": obj.object_type,
                    "ParentId": obj.parent_id,
                    "ParentWebId": obj.parent_web_id,
                    "ParentWebUrl": obj.parent_web_url,
                },
            )
            element = ET.SubElement(sp, _q(MANIFEST_NS, obj.element))
            _set(element, obj.attributes)
            if obj.versions:
                versions = ET.SubElement(element, _q(MANIFEST_NS, "Versions"))
                for version in obj.versions:
                    _set(ET.SubElement(versions, _q(MANIFEST_NS, "File")), version)
        return _serialize(root, MANIFEST_NS)


@dataclass
class DeploymentObject:
    """A ``<DeploymentObject>`` entry in ``ExportSettings.xml``."""

    id: str
    type: str  # List | Web | ...
    parent_id: str | None = None


@dataclass
class ExportSettings:
    """The required ``ExportSettings.xml`` document."""

    site_url: str
    source_type: str = "SharePointOnline"
    include_security: str = "None"
    file_location: str | None = None
    detailed_source: str | None = None
    export_objects: list[DeploymentObject] = field(default_factory=list)

    def to_xml(self) -> bytes:
        root = ET.Element(_q(EXPORT_SETTINGS_NS, "ExportSettings"))
        _set(
            root,
            {
                "SiteUrl": self.site_url,
                "FileLocation": self.file_location,
                "IncludeSecurity": self.include_security,
                "SourceType": self.source_type,
                "DetailedSource": self.detailed_source,
            },
        )
        if self.export_objects:
            objects = ET.SubElement(root, _q(EXPORT_SETTINGS_NS, "ExportObjects"))
            for obj in self.export_objects:
                _set(
                    ET.SubElement(objects, _q(EXPORT_SETTINGS_NS, "DeploymentObject")),
                    {"Id": obj.id, "Type": obj.type, "ParentId": obj.parent_id},
                )
        return _serialize(root, EXPORT_SETTINGS_NS)


@dataclass
class SystemObject:
    """A ``<SystemObject>`` entry (an immutable dependent object)."""

    id: str
    type: str  # Web | List | Folder
    url: str


@dataclass
class SystemData:
    """The required ``SystemData.xml`` document."""

    manifest_files: list[str] = field(default_factory=lambda: ["Manifest.xml"])
    system_objects: list[SystemObject] = field(default_factory=list)
    root_web_only_lists: list[str] = field(default_factory=list)
    version: str = "15.0.0.0"
    build: str = "16.0.3111.1200"
    database_version: int = 11552
    site_version: str = "15"

    def to_xml(self) -> bytes:
        root = ET.Element(_q(SYSTEM_DATA_NS, "SystemData"))
        _set(
            ET.SubElement(root, _q(SYSTEM_DATA_NS, "SchemaVersion")),
            {
                "Version": self.version,
                "Build": self.build,
                "DatabaseVersion": self.database_version,
                "SiteVersion": self.site_version,
            },
        )
        manifests = ET.SubElement(root, _q(SYSTEM_DATA_NS, "ManifestFiles"))
        for name in self.manifest_files:
            _set(ET.SubElement(manifests, _q(SYSTEM_DATA_NS, "ManifestFile")), {"Name": name})
        objects = ET.SubElement(root, _q(SYSTEM_DATA_NS, "SystemObjects"))
        for obj in self.system_objects:
            _set(
                ET.SubElement(objects, _q(SYSTEM_DATA_NS, "SystemObject")),
                {"Id": obj.id, "Type": obj.type, "Url": obj.url},
            )
        ET.SubElement(root, _q(SYSTEM_DATA_NS, "RootWebOnlyLists"))
        for url in self.root_web_only_lists:
            _set(ET.SubElement(root, _q(SYSTEM_DATA_NS, "RootWebOnlyLists")), {"Url": url})
        return _serialize(root, SYSTEM_DATA_NS)


@dataclass
class User:
    """A ``<User>`` entry in ``UserGroupMap.xml``.

    ``login`` must be a UPN-based login name (``i:0#.f|membership|user@contoso.com``)
    — non-UPN emails cause unexpected behavior in SharePoint Online.
    """

    id: int
    name: str
    login: str
    email: str | None = None
    is_domain_group: bool = False
    is_site_admin: bool = False
    system_id: str | None = None
    is_deleted: bool = False
    flags: int = 0


@dataclass
class Group:
    """A ``<Group>`` entry in ``UserGroupMap.xml``."""

    id: int
    name: str
    description: str | None = None
    owner: int | None = None
    owner_is_user: bool = True
    only_allow_members_view_membership: bool = True
    members: list[int] = field(default_factory=list)


@dataclass
class UserGroupMap:
    """The required ``UserGroupMap.xml`` document (entries are optional)."""

    users: list[User] = field(default_factory=list)
    groups: list[Group] = field(default_factory=list)

    def add_user(self, user: User) -> "UserGroupMap":
        self.users.append(user)
        return self

    def to_xml(self) -> bytes:
        root = ET.Element(_q(USER_GROUP_MAP_NS, "UserGroupMap"))
        users = ET.SubElement(root, _q(USER_GROUP_MAP_NS, "Users"))
        for user in self.users:
            _set(
                ET.SubElement(users, _q(USER_GROUP_MAP_NS, "User")),
                {
                    "Id": user.id,
                    "Name": user.name,
                    "Login": user.login,
                    "Email": user.email,
                    "IsDomainGroup": user.is_domain_group,
                    "IsSiteAdmin": user.is_site_admin,
                    "SystemId": user.system_id,
                    "IsDeleted": user.is_deleted,
                    "Flags": user.flags,
                },
            )
        groups = ET.SubElement(root, _q(USER_GROUP_MAP_NS, "Groups"))
        for group in self.groups:
            element = ET.SubElement(groups, _q(USER_GROUP_MAP_NS, "Group"))
            _set(
                element,
                {
                    "Id": group.id,
                    "Name": group.name,
                    "Description": group.description,
                    "Owner": group.owner,
                    "OwnerIsUser": group.owner_is_user,
                    "OnlyAllowMembersViewMembership": group.only_allow_members_view_membership,
                },
            )
            for member_id in group.members:
                _set(ET.SubElement(element, _q(USER_GROUP_MAP_NS, "Member")), {"UserId": member_id})
        return _serialize(root, USER_GROUP_MAP_NS)
