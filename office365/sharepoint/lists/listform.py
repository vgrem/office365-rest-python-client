from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ListForm(ClientValue):
    HasSourceField: Optional[bool] = None
    Id: Optional[str] = None
    SchemaJSON: Optional[str] = None
