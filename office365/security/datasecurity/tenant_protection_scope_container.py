from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.permissions import require_permission
from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.intune.devices.device_metadata import DeviceMetadata
    from office365.security.datasecurity.integrated_application_metadata import IntegratedApplicationMetadata
    from office365.security.datasecurity.policy_location import PolicyLocation
    from office365.security.datasecurity.policy_tenant_scope import PolicyTenantScope
    from office365.security.policypivotproperty import PolicyPivotProperty
    from office365.security.useractivitytypes import UserActivityTypes


class TenantProtectionScopeContainer(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TenantProtectionScopeContainer"

    @verb(role="action", effect="write")
    @require_permission(delegated=["ProtectionScopes.Compute.All"], application=["ProtectionScopes.Compute.All"])
    def compute(
        self,
        activities: UserActivityTypes,
        locations: ClientValueCollection[PolicyLocation],
        pivot_on: PolicyPivotProperty,
        device_metadata: DeviceMetadata,
        integrated_app_metadata: IntegratedApplicationMetadata,
    ) -> ClientResult[ClientValueCollection[PolicyTenantScope]]:
        """compute operation.

        Args:
            activities (UserActivityTypes):
                activities parameter
            locations (ClientValueCollection[PolicyLocation]):
                locations parameter
            pivot_on (PolicyPivotProperty):
                pivotOn parameter
            device_metadata (DeviceMetadata):
                deviceMetadata parameter
            integrated_app_metadata (IntegratedApplicationMetadata):
                integratedAppMetadata parameter
        """
        from office365.security.datasecurity.policy_tenant_scope import PolicyTenantScope

        return_type = ClientResult(self.context, ClientValueCollection(PolicyTenantScope))
        qry = ServiceOperationQuery(
            self,
            "compute",
            None,
            {
                "activities": activities,
                "locations": locations,
                "pivotOn": pivot_on,
                "deviceMetadata": device_metadata,
                "integratedAppMetadata": integrated_app_metadata,
            },
            None,
            return_type,
        )
        self.context.add_query(qry)
        return return_type
