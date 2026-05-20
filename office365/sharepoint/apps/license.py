from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AppLicense(ClientValue):
    """Specifies a marketplace license."""

    RawXMLLicenseToken: Optional[str] = None
