from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AppProperties(ClientValue):
    AppSettingsEnabled: Optional[bool] = None
    Description: Optional[str] = None
    EulaUrl: Optional[str] = None
    IsAnonymous: Optional[bool] = None
    IsDisabled: Optional[bool] = None
    ManagedDeploymentEnabled: Optional[bool] = None
    ManagePermissionsEnabled: Optional[bool] = None
    ManageSeatsEnabled: Optional[bool] = None
    MonitoringEnabled: Optional[bool] = None
    Publisher: Optional[str] = None
    RemoveEnabled: Optional[bool] = None
    SideLoadEnabled: Optional[bool] = None
    SupportUrl: Optional[str] = None
    ViewInMarketPlaceEnabled: Optional[bool] = None
