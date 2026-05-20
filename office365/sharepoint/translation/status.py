from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath


@dataclass
class TranslationStatus(ClientValue):
    Culture: Optional[str] = None
    FileStatus: Optional[int] = None
    HasPublishedVersion: Optional[bool] = None
    LastModified: Optional[datetime] = None
    Path: ResourcePath = field(default_factory=ResourcePath)
    Title: Optional[str] = None
