from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.documents.destinationlibraryinfo import DestinationLibraryInfo
from office365.sharepoint.documents.effectivebasepermissions import EffectiveBasePermissions
from office365.sharepoint.documents.librarydetails import LibraryDetails


@dataclass
class AgreementsSolutionFileContext(ClientValue):
    CategoryTermSetId: str | None = None
    CheckOutType: int | None = None
    CurrentVersion: str | None = None
    DoesUserHaveEditPermissionOnParent: bool | None = None
    EffectiveBasePermissions: EffectiveBasePermissions = field(default_factory=EffectiveBasePermissions)
    FieldLibrary: LibraryDetails = field(default_factory=LibraryDetails)
    FileProperties: dict | None = field(default_factory=dict)
    FileRelativePath: str | None = None
    FolderPathFullUrl: str | None = None
    IsAgreementsSolutionFile: bool | None = None
    LastPublishedVersion: str | None = None
    ListId: str | None = None
    ListItemId: str | None = None
    ListItemProperties: dict | None = field(default_factory=dict)
    ListItemUniqueId: str | None = None
    ModernTemplateLibrary: LibraryDetails = field(default_factory=LibraryDetails)
    ParentLibrary: LibraryDetails = field(default_factory=LibraryDetails)
    SiteId: str | None = None
    SnippetLibrary: LibraryDetails = field(default_factory=LibraryDetails)
    TargetLibrary: DestinationLibraryInfo = field(default_factory=DestinationLibraryInfo)
    WebId: str | None = None
    WebServerRelativeUrl: str | None = None
    WebUrl: str | None = None
