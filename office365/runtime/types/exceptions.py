from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from office365.runtime.client_object import ClientObject


class NotFoundException(Exception):
    """Exception raised when a requested entity is not found."""

    def __init__(self, entity: ClientObject = None, query: str = None):
        """
        Initialize a new instance of NotFoundException.

        Args:
            entity: The client object that was not found (optional)
            query: The query or filter that resulted in not finding the entity (optional)
        """
        self.entity = entity
        self.query = query

    def __str__(self):
        """User-friendly string representation of the exception."""
        if self.entity is None:
            message = "Entity not found"
        else:
            message = "{0} not found".format(self.entity.entity_type_name)

        if self.query is not None:
            message = "{0} for query: {1}".format(message, self.query)
        return message
