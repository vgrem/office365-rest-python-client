from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SmtpServer(ClientValue):
    IsReadOnly: bool | None = None
    Value: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SmtpServer"
