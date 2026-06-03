from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.entitlementmanagement.accesspackage.catalogstate import (
    AccessPackageCatalogState,
)
from office365.directory.identitygovernance.entitlementmanagement.accesspackage.catalogtype import (
    AccessPackageCatalogType,
)
from office365.directory.identitygovernance.workflow.custom_callout_extension import CustomCalloutExtension
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class AccessPackageCatalog(Entity):
    """In Microsoft Entra entitlement management, an access package catalog is a container for zero or more access
    packages. Microsoft Entra entitlement management includes a built-in catalog named General.

     An access package catalog might also have linked resources that are used in those access packages
     to provide access. To view or change the membership of catalog-scoped roles, use the role assignments API
     with the entitlement management RBAC provider."""

    @property
    def catalog_type(self) -> AccessPackageCatalogType:
        """Gets the catalogType property"""
        return self.properties.get("catalogType", AccessPackageCatalogType.userManaged)

    @property
    def created_date_time(self) -> datetime:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @property
    def is_externally_visible(self) -> Optional[bool]:
        """Gets the isExternallyVisible property"""
        return self.properties.get("isExternallyVisible", None)

    @property
    def modified_date_time(self) -> datetime:
        """Gets the modifiedDateTime property"""
        return self.properties.get("modifiedDateTime", datetime.min)

    @property
    def state(self) -> AccessPackageCatalogState:
        """Gets the state property"""
        return self.properties.get("state", AccessPackageCatalogState.unpublished)

    @property
    def custom_workflow_extensions(self) -> EntityCollection[CustomCalloutExtension]:
        """Gets the customWorkflowExtensions property"""
        return self.properties.get(
            "customWorkflowExtensions",
            EntityCollection[CustomCalloutExtension](
                self.context, CustomCalloutExtension, ResourcePath("customWorkflowExtensions", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AccessPackageCatalog"
