from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class DefaultColumnValue(ClientValue):
    """The defaultColumnValue on a columnDefinition resource specifies the default value for this column.
    The default value can either be specified directly or as a formula."""

    formula: str | None = None
    value: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DefaultColumnValue"
