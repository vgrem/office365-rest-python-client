from __future__ import annotations

from office365.runtime.client_value import ClientValue


class TenantInformation(ClientValue):
    """Information about your Azure AD tenant that is publicly displayed to users in other Azure AD tenants."""

    def __init__(
        self,
        default_domain_name: str | None = None,
        display_name: str | None = None,
        federation_brand_name: str | None = None,
        tenant_id: str | None = None,
    ):
        """
        :param str default_domain_name: Primary domain name of an Azure AD tenant.
        :param str display_name: Display name of an Azure AD tenant.
        :param str federation_brand_name: Name shown to users that sign in to an Azure AD tenant.
        :param str tenant_id: Unique identifier of an Azure AD tenant.
        """
        self.defaultDomainName = default_domain_name
        self.displayName = display_name
        self.federationBrandName = federation_brand_name
        self.tenantId = tenant_id
