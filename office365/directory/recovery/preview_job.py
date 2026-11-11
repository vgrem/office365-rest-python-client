from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.permissions import require_permission
from office365.runtime.queries.function import FunctionQuery

if TYPE_CHECKING:
    from office365.directory.recovery.change_object_base import RecoveryChangeObjectBase


class RecoveryPreviewJob(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.entraRecoveryServices.RecoveryPreviewJob"

    @require_permission(delegated=["EntraBackup.Read.All"], application=["EntraBackup.Read.All"])
    def get_changes(self) -> EntityCollection[RecoveryChangeObjectBase]:
        """getChanges operation."""
        from office365.directory.recovery.change_object_base import RecoveryChangeObjectBase

        return_type = EntityCollection(self.context, RecoveryChangeObjectBase)
        qry = FunctionQuery(self, "getChanges", None, return_type)
        self.context.add_query(qry)
        return return_type
