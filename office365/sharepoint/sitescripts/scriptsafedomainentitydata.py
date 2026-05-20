from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ScriptSafeDomainEntityData(ClientValue):
    """Microsoft.SharePoint.Client.ScriptSafeDomainEntityData is not applicable"""

    domain_name: Optional[str] = None
