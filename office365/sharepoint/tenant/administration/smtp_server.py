from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SmtpServer(ClientValue):
    """Args:
    value (str):
    is_readonly (bool):
    """

    Value = None
    IsReadOnly: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SmtpServer"
