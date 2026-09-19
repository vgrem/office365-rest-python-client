from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity


class AppCollection(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.AppServices.AppCollection"

    def get_apps_from_store(self, add_in_type: str, query_string: str) -> ClientResult[str]:
        """GetAppsFromStore operation.

        Args:
            add_in_type (str): addInType parameter
            query_string (str): queryString parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "GetAppsFromStore", [add_in_type, query_string], return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_type(self, type_: str) -> ClientResult[str]:
        """GetByType operation.

        Args:
            type_ (str): type parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "GetByType", [type_], return_type)
        self.context.add_query(qry)
        return return_type
