from office365.entity_collection import EntityCollection
from office365.intune.devices.management.managed.managed import ManagedDevice


class ManagedDeviceCollection(EntityCollection[ManagedDevice]):
    """Managed devices collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, ManagedDevice, resource_path)

    def get_by_name(self, device_name: str) -> ManagedDevice:
        """Queue a lookup of a managed device by its exact ``deviceName``.

        Intune supports ``$filter`` on ``deviceName`` (``eq`` and ``contains``),
        so the match happens server-side. Deferred — run with
        ``execute_query()``; the returned device is left uninitialized when no
        device has that name (check
        :attr:`~office365.runtime.client_object.ClientObject.is_loaded`).

        Args:
            device_name (str): The device name
        """
        escaped = device_name.replace("'", "''")
        return self.first_or_none(f"deviceName eq '{escaped}'")
