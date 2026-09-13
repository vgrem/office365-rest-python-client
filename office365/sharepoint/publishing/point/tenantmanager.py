from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity


class PointPublishingTenantManager(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.Publishing.PointPublishingTenantManager"

    def is_blog_enabled(self) -> ClientResult[bool]:
        """IsBlogEnabled operation."""
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "IsBlogEnabled", [], return_type)
        self.context.add_query(qry)
        return return_type
