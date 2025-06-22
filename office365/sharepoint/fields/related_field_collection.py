from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.fields.related_field import RelatedField


class RelatedFieldCollection(EntityCollection[RelatedField]):
    """Represents a collection of RelatedField resources."""

    def __init__(self, context, resource_path=None):
        super(RelatedFieldCollection, self).__init__(
            context, RelatedField, resource_path
        )

    def get_by_field_id(self, id_: str) -> RelatedField:
        """Gets the RelatedField with the specified ID."""
        return RelatedField(
            self.context,
            ServiceOperationPath("GetByFieldId", [id_], self.resource_path),
        )
