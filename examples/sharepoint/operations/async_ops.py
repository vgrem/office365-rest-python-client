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

import time
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_id, test_client_secret, test_tenant, create_unique_name


def poll_operation(op, label: str, max_wait_min: int = 10) -> bool:
    """Poll a SpoOperation until it completes or times out.

    Uses the server-recommended polling interval when available.

    Args:
        op: The SpoOperation to poll
        label: Human-readable label for progress output
        max_wait_min: Maximum minutes to wait

    Returns:
        True if completed successfully, False if timed out or failed.
    """
    timeout = time.time() + max_wait_min * 60

    while time.time() < timeout:
        op = ctx.load(op).execute_query()

        if op.is_complete is True:
            print(f"  ✓ {label} — completed")
            return True

        if op.has_timedout:
            print(f"  ⚠ {label} — timed out by server")
            return False

        interval = op.polling_interval_secs or 5
        print(f"  {label} — polling (next check in {interval}s)...")
        time.sleep(interval)

    print(f"  ✗ {label} — timed out after {max_wait_min} min")
    return False


def main():
    global ctx
    ctx = ClientContext(test_admin_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
    tenant = Tenant(ctx)

    # -- Step 1: create a site (async) --
    site_name = create_unique_name("AsyncDemoSite")
    site_url = f"https://{test_tenant.split('.')[0]}.sharepoint.com/sites/{site_name}"
    owner = "admin@contoso.onmicrosoft.com"

    print(f"Creating site '{site_name}'...")
    op = tenant.create_site(url=site_url, owner=owner, title=site_name).execute_query()
    created = poll_operation(op, "Create site")
    if not created:
        sys.exit(1)

    # -- Step 2: update site properties (async) --
    properties = (
        tenant.get_site_properties_by_url(site_url, include_detail=True).execute_query()
    )
    properties.set_property("SharingCapability", "ExternalUserSharingOnly")
    op = properties.update_ex().execute_query()
    poll_operation(op, "Update site properties")

    # -- Step 3: delete the site (async) --
    print("\nDeleting site...")
    op = tenant.remove_site(site_url).execute_query()
    deleted = poll_operation(op, "Delete site")

    print(f"\n{'✅' if created and deleted else '❌'} Async operations complete.")


if __name__ == "__main__":
    main()
