"""
Find OneDrive for Business sites that belong to users no longer
active in the tenant (deleted or blocked users).

Cross-references OneDrive site collections with Entra ID user
account status to identify orphaned storage that might need
cleanup, data migration, or retention hold.

Inspired by Find-OrphanOneDriveSites.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Sites.Read.All                  Read OneDrive site properties
    User.Read.All                   Read user account status
    Directory.Read.All              Read user directory info

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.graph_client import GraphClient
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import (
    test_admin_site_url,
    test_client_id,
    test_client_secret,
    test_tenant,
)


def get_inactive_users(graph_client: GraphClient) -> set:
    """Get set of user principal names for deleted or blocked users.

    Returns a set of UPNs that should be considered inactive.
    """
    inactive = set()
    try:
        # Deleted users
        deleted = graph_client.directory.deleted_items.users.get().execute_query()
        for user in deleted:
            if hasattr(user, "user_principal_name") and user.user_principal_name:
                inactive.add(user.user_principal_name)

        # Active but blocked users
        users = graph_client.users.get().execute_query()
        for user in users:
            if hasattr(user, "account_enabled") and user.account_enabled is False:
                if hasattr(user, "user_principal_name") and user.user_principal_name:
                    inactive.add(user.user_principal_name)
    except Exception as e:
        print(f"  Warning: could not fetch user data: {e}")

    return inactive


def find_orphan_onedrives() -> list[dict]:
    """Find OneDrive sites belonging to inactive (deleted/blocked) users.

    Returns:
        List of orphan OneDrive site details.
    """
    ctx = ClientContext(test_admin_site_url).with_client_secret(
        test_tenant, test_client_id, test_client_secret
    )
    admin = Tenant(ctx)

    # Also connect Graph to check user status
    graph = GraphClient(tenant=test_tenant).with_client_secret(
        test_client_id, test_client_secret
    )

    print("Fetching inactive users...")
    inactive_users = get_inactive_users(graph)
    print(f"  Found {len(inactive_users)} inactive users")

    print("Fetching OneDrive sites...")
    sites = admin.get_site_properties_from_sharepoint().execute_query()
    orphans = []

    for site in sites:
        template = getattr(site, "template", "")
        # OneDrive sites use template "SPSPERS#10" or contain "my.sharepoint"
        if template != "SPSPERS#10" and "my.sharepoint.com" not in getattr(site, "url", ""):
            continue

        # Extract user principal name from the OneDrive URL
        # e.g. https://tenant-my.sharepoint.com/personal/user_domain_com
        url = getattr(site, "url", "")
        user_upn = url.rsplit("/", 1)[-1].replace("_", "@") if "/" in url else url

        if user_upn in inactive_users:
            orphans.append({
                "url": url,
                "storage_mb": getattr(site, "storage_usage_current", 0),
                "user": user_upn,
            })

    return orphans


def main():
    print("Searching for orphan OneDrive sites...\n")
    orphans = find_orphan_onedrives()

    if not orphans:
        print("No orphan OneDrive sites found.")
        return

    total_storage = sum(o["storage_mb"] for o in orphans)
    print(f"Found {len(orphans)} orphan OneDrive sites ({total_storage} MB total):\n")
    for o in orphans:
        storage = f"{o['storage_mb']} MB" if o['storage_mb'] < 1024 else f"{o['storage_mb'] / 1024:.1f} GB"
        print(f"  {o['user']}")
        print(f"    URL:     {o['url']}")
        print(f"    Storage: {storage}")
        print()


if __name__ == "__main__":
    main()
