from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from datetime import timedelta


@value
class RuleSchedule(ClientValue):
    frequency: timedelta | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.RuleSchedule"
