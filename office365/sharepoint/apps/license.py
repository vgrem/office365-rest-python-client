from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class AppLicense(ClientValue):
    """Specifies a marketplace license."""

    RawXMLLicenseToken: Optional[str] = None
