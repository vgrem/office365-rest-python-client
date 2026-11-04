from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class WriteBackLocationModel(ClientValue):
    title: Optional[str] = None
    uri: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ESign.Models.Requests.WriteBackLocationModel"
