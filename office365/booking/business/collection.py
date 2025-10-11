from typing import Optional

from office365.booking.business.business import BookingBusiness
from office365.entity_collection import EntityCollection
from office365.outlook.mail.physical_address import PhysicalAddress


class BookingBusinessCollection(EntityCollection[BookingBusiness]):
    """"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, BookingBusiness, resource_path)

    def add(
        self, display_name: str, address: Optional[PhysicalAddress] = None, email: Optional[str] = None
    ) -> BookingBusiness:
        """
        Create a new Microsoft Bookings business in a tenant.
        :param str display_name: The business display name.
        :param PhysicalAddress address: The business display name.
        :param str email: The email address for the business.
        """
        props = {"displayName": display_name, "address": address, "email": email}
        return super().add(**props)
