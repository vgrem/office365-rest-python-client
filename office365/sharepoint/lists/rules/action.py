from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue


@dataclass
class SPRuleAction(ClientValue):
    ActionParams: dict | None = field(default_factory=dict)
    ActionType: int | None = None
