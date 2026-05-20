from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CurrencyInformation(ClientValue):
    """Information about a currency necessary for currency identification and display in the UI.

    Fields:
        DisplayString (str): The Display String (ex: $123,456.00 (United States)) for a specific currency
            which contains a sample formatted value (the currency and the number formatting from the web's locale)
            and the name of the country/region for the currency.
        LanguageCultureName (str):
        LCID (int): The LCID (locale identifier) for a specific currency.
    """

    DisplayString: Optional[str] = None
    LanguageCultureName: Optional[str] = None
    LCID: Optional[int] = None
