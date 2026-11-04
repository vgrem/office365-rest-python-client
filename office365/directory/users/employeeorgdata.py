from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class EmployeeOrgData(ClientValue):
    costCenter: str | None = None
    division: str | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.EmployeeOrgData"
