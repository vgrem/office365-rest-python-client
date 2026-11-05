from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue


class ScriptSafeDomainEntityData(ClientValue):
    """Microsoft.SharePoint.Client.ScriptSafeDomainEntityData is not applicable"""

    domain_name: Optional[str] = None
    DomainName: str | None = None
