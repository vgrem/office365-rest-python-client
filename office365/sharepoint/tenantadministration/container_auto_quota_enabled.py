from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ContainerAutoQuotaEnabled(ClientValue):
    IsReadOnly: bool | None = None
    Value: bool | None = None

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.TenantAdministration.ContainerAutoQuotaEnabled"
