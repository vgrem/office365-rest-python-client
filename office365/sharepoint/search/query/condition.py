from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.value import value


@value
class QueryCondition(ClientValue):
    """This object contains the conditions for the promoted result"""

    LCID: int | None = None
    MatchingOptions: str | None = None
    QueryConditionType: str | None = None
    SubjectTermsOrigin: str | None = None
    Terms: StringCollection = field(default_factory=StringCollection)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.QueryCondition"
