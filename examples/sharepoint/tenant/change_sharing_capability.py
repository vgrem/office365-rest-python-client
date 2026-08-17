"""
Set external sharing on site collections in Office 365

https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/set-external-sharing-on-site-collections-in-office-365
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.sharing_capabilities import (
    SharingCapabilities,
)
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, team_site_url, tenant

admin_client = ClientContext(admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

site_props = admin_client.tenant.get_site_properties_by_url(team_site_url).execute_query()

site_props.sharing_capability = SharingCapabilities.ExternalUserAndGuestSharing
site_props.update().execute_query()
