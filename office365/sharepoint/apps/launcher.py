from office365.runtime.client_result import ClientResult
from office365.runtime.queries.function import FunctionQuery
from office365.sharepoint.entity import Entity


class AppLauncher(Entity):
    """"""

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.AppLauncher.AppLauncher"

    def get_data(self, suite_version: int, is_mobile_request: bool, locale: str, on_prem_ver: str) -> ClientResult[str]:
        """GetData operation.

        Args:
            suite_version (int): suiteVersion parameter
            is_mobile_request (bool): isMobileRequest parameter
            locale (str): locale parameter
            on_prem_ver (str): onPremVer parameter
        """
        return_type = ClientResult(self.context, str())
        qry = FunctionQuery(self, "GetData", [suite_version, is_mobile_request, locale, on_prem_ver], return_type)
        self.context.add_query(qry)
        return return_type
