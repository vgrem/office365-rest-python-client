from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class ContextWebInformation(ClientValue):
    """Specifies metadata about a site."""

    FormDigestValue: Optional[str] = None
    FormDigestTimeoutSeconds: Optional[int] = None
    LibraryVersion: Optional[str] = None
    SiteFullUrl: Optional[str] = None
    SupportedSchemaVersions: StringCollection = field(default_factory=StringCollection)
    WebFullUrl: Optional[str] = None
    _valid_from: float = 0.0

    @property
    def is_valid(self):
        """
        Determines whether FormDigest has been expired or not
        """
        if self.FormDigestTimeoutSeconds is None:
            return False
        expires_in_sec = math.ceil(time.time() - self._valid_from)
        return expires_in_sec < self.FormDigestTimeoutSeconds
