"""
Gets the external sharing capability for a site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.sharing_capabilities import SharingCapabilities
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, site_url, tenant

SHARING_LABELS = {
    SharingCapabilities.Disabled: "Disabled",
    SharingCapabilities.ExternalUserSharingOnly: "Authenticated external only",
    SharingCapabilities.ExternalUserAndGuestSharing: "Anyone (links + guests)",
    SharingCapabilities.ExistingExternalUserSharingOnly: "Existing guests only",
}


def sharing_label(cap):
    if cap is None:
        return "Unknown"
    return SHARING_LABELS.get(cap, str(cap))


ctx = ClientContext(admin_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
tenant = Tenant(ctx)

props = tenant.get_site_properties_by_url(site_url).execute_query()
print(f"Site:      {site_url}")
print(f"Sharing:   {sharing_label(props.sharing_capability)}")
