from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.types.odata_property import odata
from office365.runtime.verbs import verb

if TYPE_CHECKING:
    from office365.directory.recovery.change_object_base import RecoveryChangeObjectBase


class RecoveryJob(Entity):
    @odata(name="totalFailedChanges")
    @property
    def total_failed_changes(self) -> Optional[int]:
        """Gets the totalFailedChanges property"""
        return self.properties.get("totalFailedChanges", None)

    @odata(name="totalLinksModified")
    @property
    def total_links_modified(self) -> Optional[int]:
        """Gets the totalLinksModified property"""
        return self.properties.get("totalLinksModified", None)

    @odata(name="totalObjectsModified")
    @property
    def total_objects_modified(self) -> Optional[int]:
        """Gets the totalObjectsModified property"""
        return self.properties.get("totalObjectsModified", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.entraRecoveryServices.RecoveryJob"

    @verb(role="action", effect="read")
    @require_permission(delegated=["EntraBackup.Read.All"], application=["EntraBackup.Read.All"])
    def get_failed_changes(self) -> EntityCollection[RecoveryChangeObjectBase]:
        """getFailedChanges operation."""
        from office365.directory.recovery.change_object_base import RecoveryChangeObjectBase

        return_type = EntityCollection(self.context, RecoveryChangeObjectBase)
        qry = FunctionQuery(self, "getFailedChanges", None, return_type)
        self.context.add_query(qry)
        return return_type
