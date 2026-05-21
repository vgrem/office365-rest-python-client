from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SPContainerFilterOrder(ClientValue):
    ArchiveStatus: int | None = None
    CreatedBeforeDays: int | None = None
    DeletedBeforeDays: int | None = None
    FilteringApplicationId: str | None = None
    FilteringApplicationName: str | None = None
    FilteringContainerTypeId: str | None = None
    FilteringField: int | None = None
    FilteringSensitivityLabels: StringCollection = field(default_factory=lambda: StringCollection())
    OpticalCharacterRecognitionEnabled: bool | None = None
    OwnersCount: int | None = None
    OwnershipType: int | None = None
    PrincipalOwnerIdentifier: str | None = None
    PublisherName: str | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPContainerFilterOrder"
