from __future__ import annotations

from uuid import UUID

from typing_extensions import Self

from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity


class Feature(Entity):
    """Represents an activated feature."""

    @property
    def definition_id(self) -> str | None:
        """The GUID that identifies this feature."""
        return self.properties.get("DefinitionId", None)

    @property
    def display_name(self) -> str | None:
        """The display name of this feature."""
        return self.properties.get("DisplayName", None)

    @property
    def property_ref_name(self) -> str:
        return "DefinitionId"

    def remove(self, feature_id: UUID, force: bool) -> Self:
        """Remove operation.

        Args:
            feature_id (UUID): featureId parameter
            force (bool): force parameter
        """
        qry = ServiceOperationQuery(self, "Remove", None, {"featureId": feature_id, "force": force}, None, None)
        self.context.add_query(qry)
        return self
