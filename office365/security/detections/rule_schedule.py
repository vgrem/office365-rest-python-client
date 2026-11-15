from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue

if TYPE_CHECKING:
    from datetime import timedelta


class RuleSchedule(ClientValue):
    frequency: timedelta | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.RuleSchedule"
