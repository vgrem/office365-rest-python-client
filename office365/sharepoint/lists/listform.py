from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ListForm(ClientValue):
    HasSourceField: Optional[bool] = None
    Id: Optional[str] = None
    SchemaJSON: Optional[str] = None
