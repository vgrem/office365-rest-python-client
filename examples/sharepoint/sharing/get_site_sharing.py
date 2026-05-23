"""
Gets the external sharing capability for a site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.sharing_capabilities import SharingCapabilities
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_id, test_password, test_site_url, test_tenant, test_username

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


ctx = ClientContext(test_admin_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
tenant = Tenant(ctx)

props = tenant.get_site_properties_by_url(test_site_url).execute_query()
print(f"Site:      {test_site_url}")
print(f"Sharing:   {sharing_label(props.sharing_capability)}")
