from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.booking.phone import Phone
from office365.entity import Entity
from office365.outlook.mail.physical_address import PhysicalAddress
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class BookingCustomer(Entity):
    @odata(name="addresses")
    @property
    def addresses(self) -> ClientValueCollection[PhysicalAddress]:
        """Gets the addresses property"""
        return self.properties.get("addresses", ClientValueCollection[PhysicalAddress](PhysicalAddress))

    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", datetime.min)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="emailAddress")
    @property
    def email_address(self) -> Optional[str]:
        """Gets the emailAddress property"""
        return self.properties.get("emailAddress", None)

    @odata(name="lastUpdatedDateTime")
    @property
    def last_updated_date_time(self) -> Optional[datetime]:
        """Gets the lastUpdatedDateTime property"""
        return self.properties.get("lastUpdatedDateTime", datetime.min)

    @odata(name="phones")
    @property
    def phones(self) -> ClientValueCollection[Phone]:
        """Gets the phones property"""
        return self.properties.get("phones", ClientValueCollection[Phone](Phone))

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BookingCustomer"
