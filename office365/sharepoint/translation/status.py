from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath


class TranslationStatus(ClientValue):
    def __init__(
        self,
        culture: str = None,
        file_status: int = None,
        has_published_version: bool = None,
        last_modified: datetime = None,
        path: ResourcePath = ResourcePath(),
        title: str = None,
    ):
        self.Culture = culture
        self.FileStatus = file_status
        self.HasPublishedVersion = has_published_version
        self.LastModified = last_modified
        self.Path = path
        self.Title = title
