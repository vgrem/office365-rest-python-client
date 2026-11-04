from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class RulesProperties(ClientValue):
    RulesKey: Optional[str] = None
    RulesValue: Optional[str] = None
