from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class SmtpServer(ClientValue):
    """:param str value:
    :param bool is_readonly:"""

    Value = None
    IsReadOnly: bool | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SmtpServer"
