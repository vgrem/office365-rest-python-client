from typing import Optional

from office365.runtime.client_value import ClientValue


class AppLicense(ClientValue):
    """Specifies a marketplace license."""

    RawXMLLicenseToken: Optional[str] = None
