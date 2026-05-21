from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class FieldLookupValue(ClientValue):

    """
    Specifies the value of a lookup for a fields within a list item.

    :param int lookup_id: Gets or sets the identifier (ID) of the list item that this instance of the lookup
    fields is referring to.
    :param str or None lookup_value: Gets a summary of the list item that this instance
    of the lookup fields is referring to.
    """

    LookupId: Optional[int] = None
    LookupValue: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.FieldLookupValue"