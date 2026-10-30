from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.directory.policies.unifiedrolemanagement.unifiedroleschedulerequestactions import (  # noqa: E501
    UnifiedRoleScheduleRequestActions,
)
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.objects.object import DirectoryObject
    from office365.directory.request_schedule import RequestSchedule
    from office365.directory.rolemanagement.app_scope import AppScope
    from office365.directory.rolemanagement.unifiedrole.definition import (
        UnifiedRoleDefinition,
    )
    from office365.directory.ticket_info import TicketInfo
    from office365.directory.unified_role_eligibility_schedule import (
        UnifiedRoleEligibilitySchedule,
    )


class UnifiedRoleEligibilityScheduleRequest(Entity):
    @odata(name="action")
    @property
    def action(self) -> UnifiedRoleScheduleRequestActions:
        """Gets the action property"""
        return self.properties.get("action", UnifiedRoleScheduleRequestActions.adminAssign)

    @odata(name="appScopeId")
    @property
    def app_scope_id(self) -> Optional[str]:
        """Gets the appScopeId property"""
        return self.properties.get("appScopeId", None)

    @odata(name="directoryScopeId")
    @property
    def directory_scope_id(self) -> Optional[str]:
        """Gets the directoryScopeId property"""
        return self.properties.get("directoryScopeId", None)

    @odata(name="isValidationOnly")
    @property
    def is_validation_only(self) -> Optional[bool]:
        """Gets the isValidationOnly property"""
        return self.properties.get("isValidationOnly", None)

    @odata(name="justification")
    @property
    def justification(self) -> Optional[str]:
        """Gets the justification property"""
        return self.properties.get("justification", None)

    @odata(name="principalId")
    @property
    def principal_id(self) -> Optional[str]:
        """Gets the principalId property"""
        return self.properties.get("principalId", None)

    @odata(name="roleDefinitionId")
    @property
    def role_definition_id(self) -> Optional[str]:
        """Gets the roleDefinitionId property"""
        return self.properties.get("roleDefinitionId", None)

    @odata(name="scheduleInfo")
    @property
    def schedule_info(self) -> RequestSchedule:
        """Gets the scheduleInfo property"""
        from office365.directory.request_schedule import RequestSchedule

        return self.properties.get("scheduleInfo", RequestSchedule())

    @odata(name="targetScheduleId")
    @property
    def target_schedule_id(self) -> Optional[str]:
        """Gets the targetScheduleId property"""
        return self.properties.get("targetScheduleId", None)

    @odata(name="ticketInfo")
    @property
    def ticket_info(self) -> TicketInfo:
        """Gets the ticketInfo property"""
        from office365.directory.ticket_info import TicketInfo

        return self.properties.get("ticketInfo", TicketInfo())

    @odata(name="appScope", navigation=True)
    @property
    def app_scope(self) -> AppScope:
        """Gets the appScope property"""
        from office365.directory.rolemanagement.app_scope import AppScope

        return self.properties.get("appScope", AppScope(self.context, ResourcePath("appScope", self.resource_path)))

    @odata(name="directoryScope", navigation=True)
    @property
    def directory_scope(self) -> DirectoryObject:
        """Gets the directoryScope property"""
        from office365.directory.objects.object import DirectoryObject

        return self.properties.get(
            "directoryScope", DirectoryObject(self.context, ResourcePath("directoryScope", self.resource_path))
        )

    @odata(name="principal", navigation=True)
    @property
    def principal(self) -> DirectoryObject:
        """Gets the principal property"""
        from office365.directory.objects.object import DirectoryObject

        return self.properties.get(
            "principal", DirectoryObject(self.context, ResourcePath("principal", self.resource_path))
        )

    @odata(name="roleDefinition", navigation=True)
    @property
    def role_definition(self) -> UnifiedRoleDefinition:
        """Gets the roleDefinition property"""
        from office365.directory.rolemanagement.unifiedrole.definition import (
            UnifiedRoleDefinition,
        )

        return self.properties.get(
            "roleDefinition", UnifiedRoleDefinition(self.context, ResourcePath("roleDefinition", self.resource_path))
        )

    @odata(name="targetSchedule", navigation=True)
    @property
    def target_schedule(self) -> UnifiedRoleEligibilitySchedule:
        """Gets the targetSchedule property"""
        from office365.directory.unified_role_eligibility_schedule import (
            UnifiedRoleEligibilitySchedule,
        )

        return self.properties.get(
            "targetSchedule",
            UnifiedRoleEligibilitySchedule(self.context, ResourcePath("targetSchedule", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UnifiedRoleEligibilityScheduleRequest"
