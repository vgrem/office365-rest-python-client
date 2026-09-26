from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity


class SPMultiGeoProxy(Entity):
    @property
    def entity_type_name(self) -> str:
        return "Microsoft.SharePoint.MultiGeo.SPMultiGeoProxy"

    def remote_thumbnail(self, url: str) -> ClientResult[bytes]:
        """RemoteThumbnail operation.

        Args:
            url (str): url parameter
        """
        return_type = ClientResult(self.context, bytes())
        qry = FunctionQuery(self, "RemoteThumbnail", [url], return_type, return_raw_content=True)
        self.context.add_query(qry)
        return return_type
