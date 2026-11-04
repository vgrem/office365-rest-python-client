from __future__ import annotations

from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class EngageDistributionInfo(ClientValue):
    AssetsFolderName: str | None = None
    DestinationId: str | None = None
    DistributedDate: datetime | None = None
    OwnerId: str | None = None
    RawThreadId: str | None = None
    ThreadId: str | None = None
    ThreadStarterId: str | None = None
