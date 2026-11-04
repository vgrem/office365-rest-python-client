from __future__ import annotations

from dataclasses import field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class SystemSiteLockExpirationResult(ClientValue):
    Error: int | None = None
    Expiration: datetime | None = field(default_factory=lambda: datetime.min)

    DatabaseNowUtc: datetime | None = None

    ExistingExpirationUtc: datetime | None = None

    ExistingFirstAcquiredUtc: datetime | None = None

    ExistingLockRequestor: str | None = None
