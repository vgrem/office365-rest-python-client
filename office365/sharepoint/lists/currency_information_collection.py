from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.lists.currency_information import CurrencyInformation


@dataclass
class CurrencyInformationCollection(ClientValue):
    """List of supported currencies: contains CurrencyInformation objects."""

    Items: ClientValueCollection[CurrencyInformation] = field(
        default_factory=lambda: ClientValueCollection(CurrencyInformation)
    )
