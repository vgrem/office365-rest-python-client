from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class TenantInformation(ClientValue):
    """Information about your Azure AD tenant that is publicly displayed to users in other Azure AD tenants.

    Args:
        default_domain_name (str): Primary domain name of an Azure AD tenant.
        display_name (str): Display name of an Azure AD tenant.
        federation_brand_name (str): Name shown to users that sign in to an Azure AD tenant.
        tenant_id (str): Unique identifier of an Azure AD tenant.
    """

    defaultDomainName: str | None = None
    displayName: str | None = None
    federationBrandName: str | None = None
    tenantId: str | None = None
