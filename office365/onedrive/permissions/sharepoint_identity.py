from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.directory.permissions.identity import Identity


@dataclass
class SharePointIdentity(Identity):
    """This resource extends from the identity resource to provide the ability to expose SharePoint-specific
    information; for example, loginName or SharePoint IDs."""

    loginName: Optional[str] = None
    displayName: Optional[str] = None
    id: Optional[str] = None
