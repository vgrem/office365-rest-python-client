from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.teams.schedule.change_tracked_entity import ChangeTrackedEntity


class ScheduleChangeRequest(ChangeTrackedEntity):
    """"""

    def approve(self, message: str) -> Self:
        """
        Approve an ScheduleChangeRequest object.

        :param str message: A custom approval message.
        """
        qry = ServiceOperationQuery(self, "approve", None, {"message": message})
        self.context.add_query(qry)
        return self

    def decline(self, message: str) -> Self:
        """
        :param str message: A custom approval message.
        """
        qry = ServiceOperationQuery(self, "decline", None, {"message": message})
        self.context.add_query(qry)
        return self

    @property
    def manager_action_datetime(self) -> datetime:
        """The date and time when the manager approved or declined the scheduleChangeRequest. The timestamp type
        represents date and time information using ISO 8601 format and is always in UTC.
        For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z."""
        return self.properties.get("managerActionDateTime", datetime.min)

    @property
    def manager_action_message(self) -> Optional[str]:
        """The message sent by the manager regarding the scheduleChangeRequest."""
        return self.properties.get("managerActionMessage", None)
