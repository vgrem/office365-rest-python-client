from office365.runtime.client_result import ClientResult
from office365.runtime.paths.v3.static import StaticPath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.sharepoint.directory.provider.object_data import DirectoryObjectData
from office365.sharepoint.entity import Entity


class SharePointDirectoryProvider(Entity):
    def __init__(self, context, resource_path=None):
        if resource_path is None:
            resource_path = StaticPath(
                "SP.Directory.Provider.SharePointDirectoryProvider"
            )
        super().__init__(context, resource_path)

    def check_site_availability(self, site_url):
        """"""
        from office365.sharepoint.directory.helper import SPHelper

        return SPHelper.check_site_availability(self.context, site_url)

    def read_directory_object(
        self, data: DirectoryObjectData
    ) -> ClientResult[DirectoryObjectData]:
        """"""
        return_type = ClientResult(self.context, DirectoryObjectData())
        payload = {"data": data}
        qry = ServiceOperationQuery(
            self, "ReadDirectoryObject", None, payload, None, return_type
        )
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.SharePointDirectoryProvider"
