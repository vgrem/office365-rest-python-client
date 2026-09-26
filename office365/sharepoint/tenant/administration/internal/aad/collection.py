from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.tenant.administration.internal.aad.permission_grant import SPO3rdPartyAADPermissionGrant


class SPO3rdPartyAADPermissionGrantCollection(EntityCollection[SPO3rdPartyAADPermissionGrant]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, SPO3rdPartyAADPermissionGrant, resource_path)

    def add(self, service_principal_id: str, resource: str, scope: str) -> Self:
        payload = {
            "servicePrincipalId": service_principal_id,
            "resource": resource,
            "scope": scope,
        }
        qry = ServiceOperationQuery(self, "Add", None, payload)
        self.context.add_query(qry)
        return self
