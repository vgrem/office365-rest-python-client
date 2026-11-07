from __future__ import annotations

from typing_extensions import Self

from office365.entity import Entity
from office365.runtime.queries.service_operation import ServiceOperationQuery


class WorkingTimeSchedule(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WorkingTimeSchedule"

    def end_working_time(self) -> Self:
        """endWorkingTime operation."""
        qry = ServiceOperationQuery(self, "endWorkingTime", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def start_working_time(self) -> Self:
        """startWorkingTime operation."""
        qry = ServiceOperationQuery(self, "startWorkingTime", None, {}, None, None)
        self.context.add_query(qry)
        return self
