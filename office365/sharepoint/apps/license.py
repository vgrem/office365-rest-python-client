from typing import Optional

from office365.runtime.client_value import ClientValue


class AppLicense(ClientValue):
    def __init__(self, raw_xml_license_token: Optional[str] = None):
        """Specifies a marketplace license."""
        self.RawXMLLicenseToken = raw_xml_license_token
