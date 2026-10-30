from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.teams.schedule.change_tracked_entity import ChangeTrackedEntity
from office365.teams.schedule.changerequestactor import ScheduleChangeRequestActor
from office365.teams.schedule.changestate import ScheduleChangeState


class ScheduleChangeRequest(ChangeTrackedEntity):
    """"""

    def approve(self, message: str) -> Self:
        """Approve an ScheduleChangeRequest object.

        Args:
            message (str): A custom approval message.
        """
        qry = ServiceOperationQuery(self, "approve", None, {"message": message})
        self.context.add_query(qry)
        return self

    def decline(self, message: str) -> Self:
        """Args:
        message (str): A custom approval message.
        """
        qry = ServiceOperationQuery(self, "decline", None, {"message": message})
        self.context.add_query(qry)
        return self

    @odata(name="managerActionDateTime", readonly=True)
    @property
    def manager_action_datetime(self) -> datetime:
        """The date and time when the manager approved or declined the scheduleChangeRequest. The timestamp type
        represents date and time information using ISO 8601 format and is always in UTC.
        For example, midnight UTC on Jan 1, 2014 is 2014-01-01T00:00:00Z."""
        return self.properties.get("managerActionDateTime", datetime.min)

    @odata(name="managerActionMessage")
    @property
    def manager_action_message(self) -> Optional[str]:
        """The message sent by the manager regarding the scheduleChangeRequest."""
        return self.properties.get("managerActionMessage", None)

    @odata(name="assignedTo")
    @property
    def assigned_to(self) -> ScheduleChangeRequestActor:
        """Gets the assignedTo property"""
        return self.properties.get("assignedTo", ScheduleChangeRequestActor.sender)

    @odata(name="managerUserId", readonly=True)
    @property
    def manager_user_id(self) -> Optional[str]:
        """Gets the managerUserId property"""
        return self.properties.get("managerUserId", None)

    @odata(name="senderDateTime", readonly=True)
    @property
    def sender_date_time(self) -> Optional[datetime]:
        """Gets the senderDateTime property"""
        return self.properties.get("senderDateTime", datetime.min)

    @odata(name="senderMessage")
    @property
    def sender_message(self) -> Optional[str]:
        """Gets the senderMessage property"""
        return self.properties.get("senderMessage", None)

    @odata(name="senderUserId", readonly=True)
    @property
    def sender_user_id(self) -> Optional[str]:
        """Gets the senderUserId property"""
        return self.properties.get("senderUserId", None)

    @odata(name="state")
    @property
    def state(self) -> ScheduleChangeState:
        """Gets the state property"""
        return self.properties.get("state", ScheduleChangeState.pending)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ScheduleChangeRequest"
