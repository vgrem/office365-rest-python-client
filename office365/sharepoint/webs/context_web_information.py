from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection

# Conservative fallback when the server omits FormDigestTimeoutSeconds, and a
# safety margin so a digest is refreshed before it can expire mid-flight.
_DEFAULT_TIMEOUT_SECONDS = 1800
_REFRESH_MARGIN_SECONDS = 60


@dataclass
class ContextWebInformation(ClientValue):
    """Specifies metadata about a site."""

    FormDigestValue: Optional[str] = None
    FormDigestTimeoutSeconds: Optional[int] = None
    LibraryVersion: Optional[str] = None
    SiteFullUrl: Optional[str] = None
    SupportedSchemaVersions: StringCollection = field(default_factory=StringCollection)
    WebFullUrl: Optional[str] = None
    # Set at construction time (which is when the digest is fetched/mapped);
    # excluded from the public constructor and repr.
    _valid_from: float = field(default_factory=time.time, init=False, repr=False)

    @property
    def is_valid(self) -> bool:
        """Whether the form digest is still valid (with a refresh margin)."""
        if self.FormDigestValue is None:
            return False
        timeout = self.FormDigestTimeoutSeconds or _DEFAULT_TIMEOUT_SECONDS
        elapsed = time.time() - self._valid_from
        return elapsed + _REFRESH_MARGIN_SECONDS < timeout
