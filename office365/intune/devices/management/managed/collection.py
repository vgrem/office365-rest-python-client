from office365.entity_collection import EntityCollection
from office365.intune.devices.management.managed.managed import ManagedDevice
from office365.runtime.odata.literals import escape_odata_string


class ManagedDeviceCollection(EntityCollection[ManagedDevice]):
    """Managed devices collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, ManagedDevice, resource_path)

    def find_by_name(self, device_name: str, *, required: bool = False) -> ManagedDevice:
        """Look up a managed device by its exact ``deviceName``.

        Intune supports ``$filter`` on ``deviceName`` (``eq`` and ``contains``),
        so the match happens server-side. Deferred — run with
        ``execute_query()``; the returned device is left uninitialized when no
        device has that name (check
        :attr:`~office365.runtime.client_object.ClientObject.is_loaded`). Pass
        ``required=True`` to raise instead (or on an ambiguous match).

        Args:
            device_name (str): The device name
            required (bool): Raise on a missing or ambiguous match when ``True``
        """
        return self._find_by_filter(f"deviceName eq '{escape_odata_string(device_name)}'", required=required)
