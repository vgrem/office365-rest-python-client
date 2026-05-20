from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class AlertHistoryState(ClientValue):
    """
    Stores changes made to alerts.
    """

    appId: str | None = None
    assignedTo: str | None = None
    comments: list[str] | None = None
