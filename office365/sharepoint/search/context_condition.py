from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ContextCondition(ClientValue):
    """
    This object contains properties that describe the context condition for the tenant.
    """

    ContextConditionType: str | None = None
    SourceId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ContextCondition"
