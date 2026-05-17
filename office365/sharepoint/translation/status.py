from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath


class TranslationStatus(ClientValue):
    def __init__(
        self,
        culture: Optional[str] = None,
        file_status: Optional[int] = None,
        has_published_version: Optional[bool] = None,
        last_modified: Optional[datetime] = None,
        path: ResourcePath = ResourcePath(),
        title: Optional[str] = None,
    ):
        self.Culture = culture
        self.FileStatus = file_status
        self.HasPublishedVersion = has_published_version
        self.LastModified = last_modified
        self.Path = path
        self.Title = title
