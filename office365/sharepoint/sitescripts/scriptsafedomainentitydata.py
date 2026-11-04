from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ScriptSafeDomainEntityData(ClientValue):
    """Microsoft.SharePoint.Client.ScriptSafeDomainEntityData is not applicable"""

    domain_name: Optional[str] = None
    DomainName: str | None = None
