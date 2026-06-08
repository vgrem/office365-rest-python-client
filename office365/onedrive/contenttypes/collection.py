from __future__ import annotations

from typing import Union

from office365.directory.permissions.require_permission import require_permission
from office365.entity_collection import EntityCollection
from office365.onedrive.contenttypes.content_type import ContentType
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery


class ContentTypeCollection(EntityCollection[ContentType]):
    """Content type collection"""

    def __init__(self, context, resource_path):
        super().__init__(context, ContentType, resource_path)

    @require_permission(delegated=["Sites.ReadWrite.All"], application=["Sites.ReadWrite.All"])
    def add(
        self,
        name: str,
        parent: Union[str, ContentType],
        description: str | None = None,
        group: str | None = None,
    ) -> ContentType:
        """Create a new contentType

        Args:
            name (str): The name of the content type.
            parent (str or ContentType): Parent content type or identifier.
            description (str or None): The descriptive text for the item.
            group (str or None): The name of the group this content type belongs to. Helps organize related content
              types.
        """
        return_type = ContentType(self.context)
        self.add_child(return_type)

        def _create(parent_id: str | None):
            payload = {
                "name": name,
                "base": {"id": parent_id},
                "description": description,
                "group": group,
            }
            qry = CreateEntityQuery(self, payload, return_type)
            self.context.add_query(qry)

        if isinstance(parent, ContentType):
            parent.ensure_property("id").after_execute(lambda _: _create(parent.id))
        else:
            _create(parent)

        return return_type

    @require_permission(delegated=["Sites.ReadWrite.All"], application=["Sites.ReadWrite.All"])
    def add_copy(self, content_type: str) -> ContentType:
        """Add a copy of a content type from a site to a list.

        Args:
            content_type (str): Canonical URL to the site content type that will be copied to the list.
        """
        payload = {"contentType": content_type}
        return_type = ContentType(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(self, "addCopy", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(delegated=["Sites.ReadWrite.All"], application=["Sites.ReadWrite.All"])
    def add_copy_from_content_type_hub(self, content_type_id: str) -> ContentType:
        """his method is part of the content type publishing changes to optimize the syncing of published content types
        to sites and lists, effectively switching from a "push everywhere" to "pull as needed" approach.
        The method allows users to pull content types directly from the content type hub to a site or list.

        Args:
            content_type_id (str): The ID of the content type in the content type hub that will be added to a target
              site or a list.
        """
        payload = {"contentTypeId": content_type_id}
        return_type = ContentType(self.context)
        self.add_child(return_type)
        qry = ServiceOperationQuery(self, "addCopyFromContentTypeHub", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @require_permission(
        delegated=["Sites.Read.All", "Sites.ReadWrite.All"], application=["Sites.Read.All", "Sites.ReadWrite.All"]
    )
    def get_compatible_hub_content_types(self) -> ContentTypeCollection:
        """
        Get a list of compatible content types from the content type hub that can be added to a target site or a list.

        This method is part of the content type publishing changes to optimize the syncing of published content types
        to sites and lists, effectively switching from a "push everywhere" to "pull as needed" approach.
        The method allows users to pull content types directly from the content type hub to a site or list.
        """
        return_type = ContentTypeCollection(self.context, self.resource_path)
        qry = FunctionQuery(self, "getCompatibleHubContentTypes", None, return_type)
        self.context.add_query(qry)
        return return_type
