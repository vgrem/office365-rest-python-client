from __future__ import annotations

from dataclasses import field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.odata_property import odata


class LicenseUnitsDetail(ClientValue):
    """The number of prepaid units that are enabled, locked out, suspended or in warning for a subscribed SKU.

    Args:
        enabled (int): The number of units that are enabled for the active subscription of the SKU.
        locked_out (int): The number of units that are locked out.
        suspended (int): The number of units that are suspended.
        warning (int): The number of units that are in warning status.
    """

    enabled: Optional[int] = field(default=None, metadata=odata(name="enabled"))
    locked_out: Optional[int] = field(default=None, metadata=odata(name="lockedOut"))
    suspended: Optional[int] = field(default=None, metadata=odata(name="suspended"))
    warning: Optional[int] = field(default=None, metadata=odata(name="warning"))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.LicenseUnitsDetail"
