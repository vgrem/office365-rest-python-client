from typing import Optional

from office365.runtime.client_value import ClientValue


class ListForm(ClientValue):
    HasSourceField: Optional[bool] = None
    Id: Optional[str] = None
    SchemaJSON: Optional[str] = None
