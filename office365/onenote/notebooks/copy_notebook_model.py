from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.directory.permissions.identity_set import IdentitySet
from office365.onenote.notebook_links import NotebookLinks
from office365.onenote.userrole import OnenoteUserRole
from office365.runtime.client_value import ClientValue


class CopyNotebookModel(ClientValue):
    createdBy: str | None = None
    createdByIdentity: IdentitySet = field(default_factory=IdentitySet)
    createdTime: datetime | None = None
    id: str | None = None
    isDefault: bool | None = None
    isShared: bool | None = None
    lastModifiedBy: str | None = None
    lastModifiedByIdentity: IdentitySet = field(default_factory=IdentitySet)
    lastModifiedTime: datetime | None = None
    links: NotebookLinks = field(default_factory=NotebookLinks)
    name: str | None = None
    sectionGroupsUrl: str | None = None
    sectionsUrl: str | None = None
    self: str | None = None
    userRole: OnenoteUserRole = OnenoteUserRole.Unknown

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopyNotebookModel"
