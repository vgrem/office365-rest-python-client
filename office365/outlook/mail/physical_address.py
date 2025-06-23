from typing import Optional

from office365.runtime.client_value import ClientValue


class PhysicalAddress(ClientValue):
    """The physical address of a contact."""

    def __init__(
        self,
        city: Optional[str] = None,
        country_or_region: Optional[str] = None,
        postal_code: Optional[str] = None,
        state: Optional[str] = None,
        street: Optional[str] = None,
    ) -> None:
        """
        :param city: The city.
        :param country_or_region: The country or region. It's a free-format string value, for example, "United States".
        :param postal_code: The postal code.
        :param state:
        :param street:
        """
        super(PhysicalAddress, self).__init__()
        self.city = city
        self.countryOrRegion = country_or_region
        self.postalCode = postal_code
        self.state = state
        self.street = street
