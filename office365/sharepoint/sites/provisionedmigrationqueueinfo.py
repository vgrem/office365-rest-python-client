from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ProvisionedMigrationQueueInfo(ClientValue):
    JobQueueUri: str | None = None
