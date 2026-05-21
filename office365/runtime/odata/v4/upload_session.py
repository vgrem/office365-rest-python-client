from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class UploadSession(ClientValue):
    """The UploadSession resource provides information about how to upload large files to OneDrive, OneDrive for
    Business, or SharePoint document libraries."""

    uploadUrl: str | None = None
    expirationDateTime: datetime | None = None
    nextExpectedRanges: StringCollection = field(default_factory=StringCollection)
