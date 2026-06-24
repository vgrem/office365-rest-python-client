"""
Long-running async SharePoint operations — create sites, update
properties, and poll for completion.

Every Tenant admin operation (create site, delete site, update
site properties) returns a ``SpoOperation`` object. The operation
runs asynchronously; you must poll its ``IsComplete`` property
until it finishes before taking dependent actions.

Pattern: start operation → poll with recommended interval →
confirm completion.

Requires delegated permission ``Sites.FullControl.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/tenant/SpoOperation
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.sharing_capabilities import SharingCapabilities
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import (
    create_unique_name,
    test_admin_site_url,
    test_client_id,
    test_username,
    test_tenant,
    test_password,
    test_user_principal_name_alt,
)


def main():
    ctx = ClientContext(test_admin_site_url).with_username_and_password(
        test_tenant, test_client_id, test_username, test_password
    )
    tenant = Tenant(ctx)

    # -- Step 1: create a site (async) --
    site_name = create_unique_name("AsyncDemoSite")
    site_url = f"https://{test_tenant.split('.')[0]}.sharepoint.com/sites/{site_name}"

    print(f"Creating site '{site_name}'...")
    site = tenant.create_site_sync(url=site_url, owner=test_user_principal_name_alt, title=site_name).execute_query()

    # -- Step 2: update site properties
    properties = tenant.get_site_properties_by_url(site.url, include_detail=True).execute_query()
    properties.sharing_capability = SharingCapabilities.ExternalUserSharingOnly
    properties.update_ex().execute_query()

    # -- Step 3: delete the site (async) --
    print("\nDeleting site...")
    tenant.remove_site_sync(site_url).execute_query()


if __name__ == "__main__":
    main()
