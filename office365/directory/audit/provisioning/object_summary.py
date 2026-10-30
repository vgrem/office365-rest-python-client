from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.audit.initiator import Initiator
from office365.directory.audit.provisioning.action import ProvisioningAction
from office365.directory.audit.provisioning.provisionedidentity import (
    ProvisionedIdentity,
)
from office365.directory.audit.provisioning.service_principal import (
    ProvisioningServicePrincipal,
)
from office365.directory.audit.provisioning.statusinfo import ProvisioningStatusInfo
from office365.directory.audit.provisioning.step import ProvisioningStep
from office365.directory.audit.provisioning.system import ProvisioningSystem
from office365.directory.modified_property import ModifiedProperty
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class ProvisioningObjectSummary(Entity):
    """Represents an action performed by the Azure AD Provisioning service and its associated properties."""

    @odata(name="activityDateTime")
    @property
    def activity_datetime(self) -> datetime:
        """Represents date and time information using ISO 8601 format and is always in UTC time."""
        return self.properties.get("activityDateTime", datetime.min)

    @odata(name="changeId")
    @property
    def change_id(self) -> Optional[str]:
        """Unique ID of this change in this cycle. Supports $filter (eq, contains)."""
        return self.properties.get("changeId", None)

    @odata(name="cycleId")
    @property
    def cycle_id(self) -> Optional[str]:
        """Unique ID per job iteration. Supports $filter (eq, contains)."""
        return self.properties.get("cycleId", None)

    @odata(name="durationInMilliseconds")
    @property
    def duration_in_milliseconds(self) -> Optional[int]:
        """Indicates how long this provisioning action took to finish. Measured in milliseconds."""
        return self.properties.get("durationInMilliseconds", None)

    @odata(name="servicePrincipal")
    @property
    def service_principal(self):
        """Represents the service principal used for provisioning."""
        return self.properties.get("servicePrincipal", ProvisioningServicePrincipal())

    @property
    def activity_date_time(self) -> Optional[datetime]:
        """Gets the activityDateTime property"""
        return self.properties.get("activityDateTime", datetime.min)

    @odata(name="initiatedBy")
    @property
    def initiated_by(self) -> Initiator:
        """Gets the initiatedBy property"""
        return self.properties.get("initiatedBy", Initiator())

    @odata(name="jobId")
    @property
    def job_id(self) -> Optional[str]:
        """Gets the jobId property"""
        return self.properties.get("jobId", None)

    @odata(name="provisioningAction")
    @property
    def provisioning_action(self) -> ProvisioningAction:
        """Gets the provisioningAction property"""
        return self.properties.get("provisioningAction", ProvisioningAction.other)

    @odata(name="provisioningStatusInfo")
    @property
    def provisioning_status_info(self) -> ProvisioningStatusInfo:
        """Gets the provisioningStatusInfo property"""
        return self.properties.get("provisioningStatusInfo", ProvisioningStatusInfo())

    @odata(name="provisioningSteps")
    @property
    def provisioning_steps(self) -> ClientValueCollection[ProvisioningStep]:
        """Gets the provisioningSteps property"""
        return self.properties.get("provisioningSteps", ClientValueCollection[ProvisioningStep](ProvisioningStep))

    @odata(name="sourceIdentity")
    @property
    def source_identity(self) -> ProvisionedIdentity:
        """Gets the sourceIdentity property"""
        return self.properties.get("sourceIdentity", ProvisionedIdentity())

    @odata(name="sourceSystem")
    @property
    def source_system(self) -> ProvisioningSystem:
        """Gets the sourceSystem property"""
        return self.properties.get("sourceSystem", ProvisioningSystem())

    @odata(name="targetIdentity")
    @property
    def target_identity(self) -> ProvisionedIdentity:
        """Gets the targetIdentity property"""
        return self.properties.get("targetIdentity", ProvisionedIdentity())

    @odata(name="targetSystem")
    @property
    def target_system(self) -> ProvisioningSystem:
        """Gets the targetSystem property"""
        return self.properties.get("targetSystem", ProvisioningSystem())

    @odata(name="tenantId")
    @property
    def tenant_id(self) -> Optional[str]:
        """Gets the tenantId property"""
        return self.properties.get("tenantId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ProvisioningObjectSummary"

    @odata(name="modifiedProperties")
    @property
    def modified_properties(self) -> ClientValueCollection[ModifiedProperty]:
        """Gets the modifiedProperties property"""
        return self.properties.get("modifiedProperties", ClientValueCollection[ModifiedProperty](ModifiedProperty))
