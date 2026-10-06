from typing import Optional

from office365.booking.business.business import BookingBusiness
from office365.entity_collection import EntityCollection
from office365.outlook.mail.physical_address import PhysicalAddress


class BookingBusinessCollection(EntityCollection[BookingBusiness]):
    """"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, BookingBusiness, resource_path)

    def get_by_name(self, display_name: str) -> BookingBusiness:
        """Queue a lookup of a booking business by its ``displayName``.

        ``GET /solutions/bookingBusinesses`` only returns ``id`` and
        ``displayName`` and supports neither ``$filter`` nor ``$top``, so the
        collection is fetched and matched client-side. Deferred — run with
        ``execute_query()``; the returned business is left uninitialized when no
        business has that name (check
        :attr:`~office365.runtime.client_object.ClientObject.is_loaded`). Fetch
        the full record with a subsequent ``get()``.

        Args:
            display_name (str): The business display name
        """
        return_type = self.create_typed_object()
        self.add_child(return_type)

        def _match(col: BookingBusinessCollection) -> None:
            match = next((b for b in col if b.get_property("displayName") == display_name), None)
            if match is None:
                return
            for k, v in match.properties.items():
                return_type.set_property(k, v, False)

        self.get().after_execute(_match)
        return return_type

    def add(
        self, display_name: str, address: Optional[PhysicalAddress] = None, email: Optional[str] = None
    ) -> BookingBusiness:
        """Create a new Microsoft Bookings business in a tenant.

        Args:
            display_name (str): The business display name.
            address (PhysicalAddress): The business display name.
            email (str): The email address for the business.
        """
        props = {"displayName": display_name, "address": address, "email": email}
        return super().add(**props)
