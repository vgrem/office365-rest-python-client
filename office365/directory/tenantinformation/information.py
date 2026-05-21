from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TenantInformation(ClientValue):
    """Information about your Azure AD tenant that is publicly displayed to users in other Azure AD tenants.

    :param str default_domain_name: Primary domain name of an Azure AD tenant.
    :param str display_name: Display name of an Azure AD tenant.
    :param str federation_brand_name: Name shown to users that sign in to an Azure AD tenant.
    :param str tenant_id: Unique identifier of an Azure AD tenant.
    """

    defaultDomainName: str | None = None
    displayName: str | None = None
    federationBrandName: str | None = None
    tenantId: str | None = None
