from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ScriptSafeDomainEntityData(ClientValue):
    """Microsoft.SharePoint.Client.ScriptSafeDomainEntityData is not applicable"""

    domain_name: Optional[str] = None
    DomainName: str | None = None
