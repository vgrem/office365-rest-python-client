from __future__ import annotations

from office365.runtime.client_value import ClientValue


class EnqueueJobInformation(ClientValue):
    EnqueueJobStatus: int | None = None
    Message: str | None = None
