from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath


@dataclass
class DashboardItem(ClientValue):
    WebAbsolutePath: SPResPath = field(default_factory=SPResPath)
