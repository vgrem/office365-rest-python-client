from __future__ import annotations

from office365.runtime.client_value import ClientValue


class SharePointEmbeddedClientLogProperties(ClientValue):
    Identifier: str | None = None
    LogMessage: str | None = None
    LogType: int | None = None
    Operation: int | None = None
    OperationStatus: int | None = None

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SharePointEmbeddedClientLogProperties"
