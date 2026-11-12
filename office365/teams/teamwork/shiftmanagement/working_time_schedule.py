from __future__ import annotations

from typing_extensions import Self

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.verbs import verb


class WorkingTimeSchedule(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkingTimeSchedule"

    @verb(role="action", effect="write")
    @require_permission(application=["Schedule-WorkingTime.ReadWrite.All"])
    def end_working_time(self) -> Self:
        """endWorkingTime operation."""
        qry = ServiceOperationQuery(self, "endWorkingTime", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(application=["Schedule-WorkingTime.ReadWrite.All"])
    def start_working_time(self) -> Self:
        """startWorkingTime operation."""
        qry = ServiceOperationQuery(self, "startWorkingTime", None, {}, None, None)
        self.context.add_query(qry)
        return self
