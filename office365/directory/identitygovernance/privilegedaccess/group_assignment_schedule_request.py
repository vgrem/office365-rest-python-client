from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.directory.identitygovernance.privilegedaccess.group_eligibility_schedule import (
    PrivilegedAccessGroupEligibilitySchedule,
)
from office365.directory.identitygovernance.privilegedaccess.grouprelationships import PrivilegedAccessGroupRelationships
from office365.directory.objects.object import DirectoryObject
from office365.entity import Entity
from office365.onedrive.termstore.groups.group import Group
from office365.permissions import require_permission
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.directory.identitygovernance.privilegedaccess.group_assignment_schedule_request import (
        PrivilegedAccessGroupAssignmentScheduleRequest,
    )
    from office365.directory.request_schedule import RequestSchedule
    from office365.security.evaluation_outcome import EvaluationOutcome


class PrivilegedAccessGroupAssignmentScheduleRequest(Entity):
    @odata(name="accessId")
    @property
    def access_id(self) -> PrivilegedAccessGroupRelationships:
        """Gets the accessId property"""
        return self.properties.get("accessId", PrivilegedAccessGroupRelationships.owner)

    @odata(name="groupId")
    @property
    def group_id(self) -> Optional[str]:
        """Gets the groupId property"""
        return self.properties.get("groupId", None)

    @odata(name="principalId")
    @property
    def principal_id(self) -> Optional[str]:
        """Gets the principalId property"""
        return self.properties.get("principalId", None)

    @odata(name="targetScheduleId")
    @property
    def target_schedule_id(self) -> Optional[str]:
        """Gets the targetScheduleId property"""
        return self.properties.get("targetScheduleId", None)

    @odata(name="activatedUsing", navigation=True)
    @property
    def activated_using(self) -> PrivilegedAccessGroupEligibilitySchedule:
        """Gets the activatedUsing property"""
        return self.properties.get(
            "activatedUsing",
            PrivilegedAccessGroupEligibilitySchedule(self.context, ResourcePath("activatedUsing", self.resource_path)),
        )

    @odata(name="group", navigation=True)
    @property
    def group(self) -> Group:
        """Gets the group property"""
        return self.properties.get("group", Group(self.context, ResourcePath("group", self.resource_path)))

    @odata(name="principal", navigation=True)
    @property
    def principal(self) -> DirectoryObject:
        """Gets the principal property"""
        return self.properties.get(
            "principal", DirectoryObject(self.context, ResourcePath("principal", self.resource_path))
        )

    @odata(name="targetSchedule", navigation=True)
    @property
    def target_schedule(self) -> PrivilegedAccessGroupEligibilitySchedule:
        """Gets the targetSchedule property"""
        return self.properties.get(
            "targetSchedule",
            PrivilegedAccessGroupEligibilitySchedule(self.context, ResourcePath("targetSchedule", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.PrivilegedAccessGroupAssignmentScheduleRequest"

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["PrivilegedAssignmentSchedule.ReadWrite.AzureADGroup"],
        application=["PrivilegedAssignmentSchedule.ReadWrite.AzureADGroup"],
    )
    def cancel(self) -> Self:
        """cancel operation."""
        qry = ServiceOperationQuery(self, "cancel", None, {}, None, None)
        self.context.add_query(qry)
        return self

    @verb(role="action", effect="write")
    @require_permission(
        delegated=["PrivilegedAssignmentSchedule.ReadWrite.AzureADGroup"],
        application=["PrivilegedAssignmentSchedule.ReadWrite.AzureADGroup"],
    )
    def update_request(
        self, evaluation_id: str, evaluation_outcome: EvaluationOutcome, schedule_info: RequestSchedule, reason: str
    ) -> PrivilegedAccessGroupAssignmentScheduleRequest:
        """updateRequest operation.

        Args:
            evaluation_id (str):
                evaluationId parameter
            evaluation_outcome (EvaluationOutcome):
                evaluationOutcome parameter
            schedule_info (RequestSchedule):
                scheduleInfo parameter
            reason (str):
                reason parameter
        """
        from office365.directory.identitygovernance.privilegedaccess.group_assignment_schedule_request import (
            PrivilegedAccessGroupAssignmentScheduleRequest,
        )

        return_type = PrivilegedAccessGroupAssignmentScheduleRequest(self.context)
        qry = ServiceOperationQuery(
            self,
            "updateRequest",
            None,
            {
                "evaluationId": evaluation_id,
                "evaluationOutcome": evaluation_outcome,
                "scheduleInfo": schedule_info,
                "reason": reason,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
