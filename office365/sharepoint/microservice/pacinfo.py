from typing import Optional

from office365.runtime.client_value import ClientValue


class PacInfo(ClientValue):
    def __init__(
        self,
        endpoint: Optional[str] = None,
        is_app_only: Optional[bool] = None,
        scenario: Optional[str] = None,
        token: Optional[str] = None,
        version: Optional[int] = None,
    ):
        self.Endpoint = endpoint
        self.IsAppOnly = is_app_only
        self.Scenario = scenario
        self.Token = token
        self.Version = version

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.MicroService.Internal.PacInfo"
