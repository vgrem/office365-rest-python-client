from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class UpdateGroupSitePropertiesParameters(ClientValue):
    storageMaximumLevel: int | None = None
    storageWarningLevel: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.UpdateGroupSitePropertiesParameters"
