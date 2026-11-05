from __future__ import annotations

from office365.runtime.client_value import ClientValue


class IngestionTaskKey(ClientValue):
    IngestionTableAccountKey: str | None = None
    IngestionTableAccountName: str | None = None
    JobId: str | None = None
    TaskId: str | None = None
    TenantName: str | None = None
