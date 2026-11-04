from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ActionOpenUrl(ClientValue):
    url: Optional[str] = None
