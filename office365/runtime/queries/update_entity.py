from office365.runtime.client_object import ClientObject
from office365.runtime.queries.client_query import ClientQuery


class UpdateEntityQuery(ClientQuery):
    """Represents an OData update operation for modifying an existing entity.

    This query type is used to construct and execute PATCH or PUT operations
    to update entities in an OData service. It inherits from ClientQuery
    and specializes it for update operations.
    """

    def __init__(self, update_type: ClientObject) -> None:
        """Initialize an update entity query.

        Args:
            update_type: The client object representing the entity to be updated.
                         This provides both the context and the entity data.

        Note:
            The query reuses the same client object for both source and target
            since we're updating an existing entity rather than creating new ones.
        """
        super().__init__(update_type.context, update_type, update_type)
