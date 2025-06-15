from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.paths.v4.entity import EntityPath
from office365.runtime.utilis import urlparse


class SitePath(EntityPath):
    """Resource path for addressing Site resource"""

    def __init__(self, host_name, relative_path, parent=None):
        super(SitePath, self).__init__(
            ":".join([host_name, relative_path]), parent, ResourcePath("sites")
        )

    @staticmethod
    def from_url(url, parent=None):
        url_result = urlparse(url)
        return SitePath(url_result.hostname, url_result.path, parent)
