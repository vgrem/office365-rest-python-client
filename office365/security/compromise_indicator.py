from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value
from office365.security.verdict_category import VerdictCategory


@value
class CompromiseIndicator(ClientValue):
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.CompromiseIndicator"

    verdict: VerdictCategory = VerdictCategory.none
