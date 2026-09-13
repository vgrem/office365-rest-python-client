from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.function import FunctionQuery
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.sitedesigns.webpartmodel import WebPartModel


class SectionDesignIdeasApi(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.SectionDesignIdeas.SectionDesignIdeasApi"

    def get_section_design_ideas(self, title: str, sub_title: str) -> ClientResult[ClientValueCollection[WebPartModel]]:
        """GetSectionDesignIdeas operation.

        Args:
            title (str): title parameter
            sub_title (str): subTitle parameter
        """
        return_type = ClientResult(self.context, ClientValueCollection[WebPartModel]())
        qry = ServiceOperationQuery(
            self, "GetSectionDesignIdeas", None, {"title": title, "subTitle": sub_title}, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    def ping(self) -> ClientResult[str]:
        """Ping operation."""
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "Ping", [], return_type)
        self.context.add_query(qry)
        return return_type
