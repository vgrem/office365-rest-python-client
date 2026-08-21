"""
Site lifecycle via the tenant admin — create, update properties, delete.

Tenant admin site operations (create/update/delete) run asynchronously on
the server; the ``*_sync`` variants used here wait for completion, so you
can take dependent actions immediately.

Pattern: create → load properties → update → delete.

Requires delegated permission ``Sites.FullControl.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/tenant/SpoOperation
"""

import argparse
import uuid

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.sharing_capabilities import SharingCapabilities
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import (
    admin_site_url,
    client_id,
    password,
    tenant,
    user_principal_alt,
    username,
)


def main():
    argparse.ArgumentParser(description="Site lifecycle via the tenant admin").parse_args()

    ctx = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    tenant_admin = Tenant(ctx)

    site_name = f"Lifecycle{uuid.uuid4().hex[:8]}"
    site_url = f"https://{tenant.split('.')[0]}.sharepoint.com/sites/{site_name}"

    print(f"Creating site '{site_name}'...")
    site = tenant_admin.create_site_sync(url=site_url, owner=user_principal_alt, title=site_name).execute_query()
    print(f"Site created: {site.url}")

    print("Updating site properties (sharing capability)...")
    assert site.url is not None
    properties = tenant_admin.get_site_properties_by_url(site.url, include_detail=True).execute_query()
    properties.sharing_capability = SharingCapabilities.ExternalUserSharingOnly
    properties.update_ex().execute_query()
    print("Sharing capability set to ExternalUserSharingOnly")

    print("Deleting site...")
    tenant_admin.remove_site_sync(site_url).execute_query()
    print("Site deleted")


if __name__ == "__main__":
    main()
