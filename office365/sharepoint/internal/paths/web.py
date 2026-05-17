from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.utilities import is_absolute_url, urlparse


class WebPath(ResourcePath):
    @property
    def segment(self):
        return "Web"

    @property
    def web_path(self):
        assert self._key is not None
        key = str(self._key)
        if is_absolute_url(key):
            url_parts = urlparse(key)
            return url_parts.path
        else:
            return key

    @property
    def parent(self):
        return None
