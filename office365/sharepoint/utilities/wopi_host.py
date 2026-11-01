from office365.runtime.client_result import ClientResult
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class WopiHostUtility(Entity):
    """ """

    @staticmethod
    @site_access(SiteLevel.WRITE)
    def generate_file_bundle(context: ClientContext) -> ClientResult[str]:
        """ """
        return_type = ClientResult(context)
        qry = ServiceOperationQuery(
            WopiHostUtility(context),
            "GenerateFileBundle",
            None,
            None,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @staticmethod
    @site_access(SiteLevel.READ)
    def get_wopi_origins(context):
        return_type = ClientResult(context, ClientValueCollection(str))
        qry = ServiceOperationQuery(
            WopiHostUtility(context),
            "GetWopiOrigins",
            None,
            None,
            None,
            return_type,
            True,
        )
        context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Utilities.WopiHostUtility"
