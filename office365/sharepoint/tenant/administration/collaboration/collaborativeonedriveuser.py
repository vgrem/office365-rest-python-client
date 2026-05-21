from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CollaborativeOneDriveUser(ClientValue):
    anonymousLinkCount: int | None = None
    fileCount: int | None = None
    filesSharedExternally: int | None = None
    filesSharedInternally: int | None = None
    totalFilesShared: int | None = None
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborativeOneDriveUser"
