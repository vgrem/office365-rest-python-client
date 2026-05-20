from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ItemActionStat(ClientValue):
    """The itemActionStat resource provides aggregate details about an action over a period of time."""

    actionCount: int | None = None
    actorCount: int | None = None
