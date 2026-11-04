from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ContextCondition(ClientValue):
    """
    This object contains properties that describe the context condition for the tenant.
    """

    ContextConditionType: str | None = None
    SourceId: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.ContextCondition"
