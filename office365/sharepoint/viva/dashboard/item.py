from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath as SPResPath


class DashboardItem(ClientValue):
    WebAbsolutePath: SPResPath = field(default_factory=SPResPath)
