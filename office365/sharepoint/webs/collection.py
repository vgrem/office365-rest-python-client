from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.internal.paths.web import WebPath
from office365.sharepoint.webs.creation_information import WebCreationInformation

if TYPE_CHECKING:
    from office365.sharepoint.client_context import ClientContext
    from office365.sharepoint.webs.web import Web


class WebCollection(EntityCollection["Web"]):
    """Web collection"""

    def __init__(
        self,
        context: ClientContext,
        resource_path: ResourcePath = None,
        parent_web: Web = None,
    ):
        from office365.sharepoint.webs.web import Web

        super().__init__(context, Web, resource_path, parent_web)

    def add(self, web_creation_information: WebCreationInformation) -> Web:
        """
        Create WebSite
        """
        from office365.sharepoint.webs.web import Web

        return_type = Web(self.context)
        self.add_child(return_type)
        payload = {"parameters": web_creation_information}
        qry = ServiceOperationQuery(self, "add", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    def create_typed_object(self, initial_properties=None, resource_path=None):
        if resource_path is None:
            resource_path = WebPath(self.resource_path)
        return super().create_typed_object(initial_properties, resource_path)

    @property
    def resource_url(self) -> str:
        val = super(WebCollection, self).resource_url
        parent_web_url = self._parent.get_property("Url")
        if parent_web_url is not None:
            val = val.replace(self.context.service_root_url, parent_web_url + "/_api")
        return val
