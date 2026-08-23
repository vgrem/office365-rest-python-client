from urllib.parse import urlparse

from office365.runtime.http.url import is_absolute_url
from office365.runtime.paths.resource_path import ResourcePath


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
