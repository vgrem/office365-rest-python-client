from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection, StringCollection


@dataclass
class SPSyntexApplicationProperties(ClientValue):
    ApplicationId: UUID | None = None
    ApplicationName: str | None = None
    Applications: GuidCollection = field(default_factory=GuidCollection)
    AppOnlyPermissions: StringCollection = field(default_factory=lambda: StringCollection())
    CopilotEmbeddedChatHosts: StringCollection = field(default_factory=lambda: StringCollection())
    DelegatedPermissions: StringCollection = field(default_factory=lambda: StringCollection())
    OverrideTenantSharingCapability: bool | None = None
    OverrideTenantSharingCapabilityNullable: int | None = None
    OwningApplicationId: UUID | None = None
    OwningApplicationName: str | None = None
    SharingCapability: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPSyntexApplicationProperties"
