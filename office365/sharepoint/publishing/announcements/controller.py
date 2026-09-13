from typing_extensions import Self

from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.publishing.announcements.data import AnnouncementsData


class AnnouncementsController(Entity):
    def __init__(self, context, path=None):
        if path is None:
            path = ResourcePath("SP.Publishing.AnnouncementsController")
        super().__init__(context, path)

    @property
    def entity_type_name(self):
        return "SP.Publishing.AnnouncementsController"

    def active(self) -> ClientResult[ClientValueCollection[AnnouncementsData]]:
        """Active operation."""
        return_type = ClientResult(self.context, ClientValueCollection[AnnouncementsData]())
        qry = FunctionQuery(self, "Active", [], return_type)
        self.context.add_query(qry)
        return return_type

    def flw_property_filtering_mapping(self, flw_property_filtering_mapping: str) -> Self:
        """FlwPropertyFilteringMapping operation.

        Args:
            flw_property_filtering_mapping (str): flwPropertyFilteringMapping parameter
        """
        qry = ServiceOperationQuery(
            self,
            "FlwPropertyFilteringMapping",
            None,
            {"flwPropertyFilteringMapping": flw_property_filtering_mapping},
            None,
            None,
        )
        self.context.add_query(qry)
        return self
