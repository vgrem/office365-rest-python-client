from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ShowNextGenerationSyncClientOnTeamSite(ClientValue):
    IsHidden: bool | None = None
    IsReadOnly: bool | None = None
    ReadOnlyReasonCode: int | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.ShowNextGenerationSyncClientOnTeamSite"
