from typing import TYPE_CHECKING

from office365.runtime.queries.client_query import ClientQuery

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject


class DeleteEntityQuery(ClientQuery):
    """A query to delete an entity from the server."""

    def __init__(self, delete_type: "ClientObject") -> None:
        """
        Initialize a delete operation for the specified entity.

        Args:
            delete_type: The client object to be deleted. Must be a valid entity
                         with a context and resource path.

        Example:
            >>> ctx = ClientContext()
            >>> file = ctx.web.get_file_by_server_relative_url()
            >>> item = file.delete_object()  # Creates a DeleteEntityQuery
            >>> ctx.execute_query()  # Executes the deletion
        """
        super().__init__(delete_type.context, delete_type)
