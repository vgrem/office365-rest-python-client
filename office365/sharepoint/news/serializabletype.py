from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SerializableType(ClientValue):
    type: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.News.DataModel.SerializableType"
