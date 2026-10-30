from typing import Optional

from office365.directory.identities.providers.base import IdentityProviderBase
from office365.runtime.types.odata_property import odata


class BuiltInIdentityProvider(IdentityProviderBase):
    """
    Represents built-in identity providers with External Identities for an Azure Active Directory tenant.
    """

    @odata(name="identityProviderType")
    @property
    def identity_provider_type(self) -> Optional[str]:
        """
        The identity provider type. For a B2B scenario, possible values: AADSignup, MicrosoftAccount, EmailOTP.
        """
        return self.properties.get("identityProviderType", None)
