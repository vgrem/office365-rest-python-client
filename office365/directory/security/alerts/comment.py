from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AlertComment(ClientValue):
    """An analyst-generated comment that is associated with an alert or incident."""

    comment: str | None = None
