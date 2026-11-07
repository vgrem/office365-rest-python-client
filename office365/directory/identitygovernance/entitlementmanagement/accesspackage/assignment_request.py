from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.answer import AccessPackageAnswer
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment import (
    AccessPackageAssignment,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.assignment_request_parameters import (  # noqa: E501
    AccessPackageAssignmentRequestParameters,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.custom_extension_callout_instance import (  # noqa: E501
    CustomExtensionCalloutInstance,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.package import (
    AccessPackage,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.requeststate import (
    AccessPackageRequestState,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.requesttype import (
    AccessPackageRequestType,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.subject import (
    AccessPackageSubject,
)
from office365.directory.identitygovernance.entitlementmanagement.schedule import EntitlementManagementSchedule
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.extensions.custom.data import CustomExtensionData


class AccessPackageAssignmentRequest(Entity):
    @odata(name="completedDateTime")
    @property
    def completed_date_time(self) -> datetime:
        """Gets the completedDateTime property"""
        return self.properties.get("completedDateTime", datetime.min)

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="justification")
    @property
    def justification(self) -> Optional[str]:
        """Gets the justification property"""
        return self.properties.get("justification", None)

    @odata(name="requestType")
    @property
    def request_type(self) -> AccessPackageRequestType:
        """Gets the requestType property"""
        return self.properties.get("requestType", AccessPackageRequestType.notSpecified)

    @odata(name="state")
    @property
    def state(self) -> AccessPackageRequestState:
        """Gets the state property"""
        return self.properties.get("state", AccessPackageRequestState.submitted)

    @odata(name="status")
    @property
    def status(self) -> Optional[str]:
        """Gets the status property"""
        return self.properties.get("status", None)

    @odata(name="accessPackage", navigation=True)
    @property
    def access_package(self) -> AccessPackage:
        """Gets the accessPackage property"""
        return self.properties.get(
            "accessPackage", AccessPackage(self.context, ResourcePath("accessPackage", self.resource_path))
        )

    @odata(name="assignment", navigation=True)
    @property
    def assignment(self) -> AccessPackageAssignment:
        """Gets the assignment property"""
        return self.properties.get(
            "assignment", AccessPackageAssignment(self.context, ResourcePath("assignment", self.resource_path))
        )

    @odata(name="requestor", navigation=True)
    @property
    def requestor(self) -> AccessPackageSubject:
        """Gets the requestor property"""
        return self.properties.get(
            "requestor", AccessPackageSubject(self.context, ResourcePath("requestor", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageAssignmentRequest"

    @odata(name="answers")
    @property
    def answers(self) -> ClientValueCollection[AccessPackageAnswer]:
        """Gets the answers property"""
        return self.properties.get("answers", ClientValueCollection[AccessPackageAnswer](AccessPackageAnswer))

    @odata(name="customExtensionCalloutInstances")
    @property
    def custom_extension_callout_instances(self) -> ClientValueCollection[CustomExtensionCalloutInstance]:
        """Gets the customExtensionCalloutInstances property"""
        return self.properties.get(
            "customExtensionCalloutInstances",
            ClientValueCollection[CustomExtensionCalloutInstance](CustomExtensionCalloutInstance),
        )

    @odata(name="parameters")
    @property
    def parameters(self) -> AccessPackageAssignmentRequestParameters:
        """Gets the parameters property"""
        return self.properties.get("parameters", AccessPackageAssignmentRequestParameters())

    @odata(name="schedule")
    @property
    def schedule(self) -> EntitlementManagementSchedule:
        """Gets the schedule property"""
        return self.properties.get("schedule", EntitlementManagementSchedule())

    def cancel(self) -> Self:
        """cancel operation."""
        qry = ServiceOperationQuery(self, "cancel", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def reprocess(self) -> Self:
        """reprocess operation."""
        qry = ServiceOperationQuery(self, "reprocess", None, {}, None, None)
        self.context.add_query(qry)
        return self

    def resume(self, source: str, type_: str, data: CustomExtensionData) -> Self:
        """resume operation.

        Args:
            source (str):
                source parameter
            type_ (str):
                type parameter
            data (CustomExtensionData):
                data parameter
        """
        qry = ServiceOperationQuery(self, "resume", None, {"source": source, "type": type_, "data": data}, None, None)
        self.context.add_query(qry)
        return self
