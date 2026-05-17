from typing import Optional

from office365.runtime.client_value import ClientValue


class EsignatureThirdPartyProvidersInfo(ClientValue):
    def __init__(self, is_enabled: Optional[bool] = None, provider_name: Optional[str] = None):
        self.IsEnabled = is_enabled
        self.ProviderName = provider_name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.EsignatureThirdPartyProvidersInfo"
