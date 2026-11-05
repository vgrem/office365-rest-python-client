from typing import Optional

from office365.runtime.client_value import ClientValue


class RulesProperties(ClientValue):
    RulesKey: Optional[str] = None
    RulesValue: Optional[str] = None
