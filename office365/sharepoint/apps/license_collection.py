from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.apps.license import AppLicense


class AppLicenseCollection(ClientValue):
    """Specifies a collection of marketplace licenses."""

    Items: ClientValueCollection[AppLicense] = field(default_factory=lambda: ClientValueCollection(AppLicense))
