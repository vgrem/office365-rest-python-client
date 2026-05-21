from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class CollaborativeUser(ClientValue):
    totalFileInteraction: int | None = None
    totalFilesSharedExternally: int | None = None
    totalFilesSharedInternally: int | None = None
    totalFilesViewedOrEdited: int | None = None
    userPrincipalName: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborativeUser"
