from datetime import datetime

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.catalog import AccessPackageCatalog
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.requeststate import (
    AccessPackageRequestState,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.requesttype import (
    AccessPackageRequestType,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.resource import AccessPackageResource
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AccessPackageResourceRequest(Entity):
    """In Microsoft Entra entitlement management, an access package resource request is a request
    to add a resource to a catalog so that the roles of the resource can be used in one or more of the catalog's
    access packages, update a resource in a catalog to have different attribute requirements, or to remove a resource
    from a catalog that is no longer needed by the access packages."""

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

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

    @odata(name="catalog", navigation=True)
    @property
    def catalog(self) -> AccessPackageCatalog:
        """Gets the catalog property"""
        return self.properties.get(
            "catalog", AccessPackageCatalog(self.context, ResourcePath("catalog", self.resource_path))
        )

    @odata(name="resource", navigation=True)
    @property
    def resource(self) -> AccessPackageResource:
        """Gets the resource property"""
        return self.properties.get(
            "resource", AccessPackageResource(self.context, ResourcePath("resource", self.resource_path))
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageResourceRequest"
