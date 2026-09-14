from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.viva.resource_link import VivaResourceLink


class VivaResources(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.EmployeeEngagement.VivaResources"

    def add_link(self, new_link: VivaResourceLink) -> ClientResult[int]:
        """AddLink operation.

        Args:
            new_link (VivaResourceLink): newLink parameter
        """
        return_type = ClientResult(self.context, int())
        qry = ServiceOperationQuery(self, "AddLink", None, {"newLink": new_link}, None, return_type)
        self.context.add_query(qry)
        return return_type

    def remove_link(self, id_: int) -> Self:
        """RemoveLink operation.

        Args:
            id_ (int): id parameter
        """
        qry = ServiceOperationQuery(self, "RemoveLink", None, {"id": id_}, None, None)
        self.context.add_query(qry)
        return self

    def reorder_link(self, link_id: int, prev_link_id: int) -> Self:
        """ReorderLink operation.

        Args:
            link_id (int): linkId parameter
            prev_link_id (int): prevLinkId parameter
        """
        qry = ServiceOperationQuery(
            self, "ReorderLink", None, {"linkId": link_id, "prevLinkId": prev_link_id}, None, None
        )
        self.context.add_query(qry)
        return self

    def update_link(self, updated_link: VivaResourceLink) -> Self:
        """UpdateLink operation.

        Args:
            updated_link (VivaResourceLink): updatedLink parameter
        """
        qry = ServiceOperationQuery(self, "UpdateLink", None, {"updatedLink": updated_link}, None, None)
        self.context.add_query(qry)
        return self

    def update_links(self, links: ClientValueCollection[VivaResourceLink]) -> Self:
        """UpdateLinks operation.

        Args:
            links (ClientValueCollection[VivaResourceLink]): links parameter
        """
        qry = ServiceOperationQuery(self, "UpdateLinks", None, {"links": links}, None, None)
        self.context.add_query(qry)
        return self
