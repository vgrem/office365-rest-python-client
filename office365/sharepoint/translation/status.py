from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.types.resource_path import ResourcePath


@dataclass
class TranslationStatus(ClientValue):
    Culture: str | None = None
    FileStatus: int | None = None
    HasPublishedVersion: bool | None = None
    LastModified: datetime | None = None
    Path: ResourcePath = field(default_factory=ResourcePath)
    Title: str | None = None
