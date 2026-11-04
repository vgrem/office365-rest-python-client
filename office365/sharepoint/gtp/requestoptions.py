from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class GptRequestOptions(ClientValue):
    BestOf: Optional[int] = None
    Prompt: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Internal.GptRequestOptions"
