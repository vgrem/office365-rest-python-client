from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ProvisionedMigrationQueueInfo(ClientValue):
    JobQueueUri: str | None = None
