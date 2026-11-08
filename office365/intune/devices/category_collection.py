from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.intune.devices.category import DeviceCategory
from office365.runtime.odata.literals import escape_odata_string


class DeviceCategoryCollection(EntityCollection[DeviceCategory]):
    """Device categories collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, DeviceCategory, resource_path)

    def find_by_display_name(self, display_name: str, *, required: bool = False) -> DeviceCategory:
        """Look up a device category by its ``displayName``.

        Deferred — run with ``execute_query()``. Tolerant by default: when no
        category matches, the returned object is left uninitialized (check
        :attr:`~office365.runtime.client_object.ClientObject.is_loaded`). Pass
        ``required=True`` to raise instead (or on an ambiguous match).

        Args:
            display_name (str): The category name an administrator gave it
            required (bool): Raise on a missing or ambiguous match when ``True``
        """
        return self._find_by_filter(f"displayName eq '{escape_odata_string(display_name)}'", required=required)
