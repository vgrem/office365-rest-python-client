from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.utilities import get_absolute_url, is_absolute_url, urlparse


@dataclass
class ResourcePath(ClientValue):
    """Represents the full (absolute) or parts (relative) path of a site collection, web, file, folder or
    other artifacts in the database.

    Args:
        decoded_url (str): Gets the path in the decoded form.
    """

    DecodedUrl: Optional[str] = None

    @staticmethod
    def create_absolute(site_url: str, path: str) -> ResourcePath:
        """Creates absolute path

        Args:
            site_url (str): Site url
            path (str): Resource path
        """
        if is_absolute_url(path):
            return ResourcePath(path)
        else:
            path = str(ResourcePath.create_relative(site_url, path))
            return ResourcePath("".join([get_absolute_url(site_url), path]))

    @staticmethod
    def create_relative(site_url: str, path: str) -> ResourcePath:
        """Creates server relative path

        Args:
            site_url (str): Site url
            path (str): Resource path
        """
        site_path = urlparse(site_url).path
        if not path.lower().startswith(site_path.lower()):
            return ResourcePath("/".join([site_path, path]))
        else:
            return ResourcePath(path)

    @property
    def entity_type_name(self) -> str:
        return "SP.ResourcePath"

    def __str__(self) -> str:
        return self.DecodedUrl or ""

    def __repr__(self) -> str:
        return self.DecodedUrl or self.entity_type_name
