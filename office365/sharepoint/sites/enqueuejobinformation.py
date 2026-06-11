from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class EnqueueJobInformation(ClientValue):
    EnqueueJobStatus: int | None = None
    Message: str | None = None
