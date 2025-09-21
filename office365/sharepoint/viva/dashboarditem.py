from office365.runtime.client_value import ClientValue
from office365.runtime.paths.resource_path import ResourcePath


class DashboardItem(ClientValue):

    def __init__(self, web_absolute_path: ResourcePath = None):
        self.web_absolute_path = web_absolute_path
