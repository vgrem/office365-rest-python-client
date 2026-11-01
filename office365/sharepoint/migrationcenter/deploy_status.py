from office365.permissions.roles import DirectoryRole
from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity
from office365.sharepoint.permissions import SiteLevel, site_access


class MigrationCenterDeployStatus(Entity):
    """"""

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.MigrationCenterDeployStatus"

    @site_access(SiteLevel.READ, role=DirectoryRole.SharePointAdministrator)
    def is_change_deployed(self, change_name: str) -> ClientResult[bool]:
        """IsChangeDeployed operation.

        Args:
            change_name (str): changeName parameter
        """
        return_type = ClientResult(self.context, bool())
        qry = FunctionQuery(self, "IsChangeDeployed", [change_name], return_type)
        self.context.add_query(qry)
        return return_type
