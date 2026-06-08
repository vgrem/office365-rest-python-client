"""
Find SharePoint Online sites with no recent content modifications.

Useful for identifying obsolete or abandoned sites that can be removed
or archived. Cross-references site activity dates with owner information
for group-connected sites.

Inspired by the PowerShell script Find-ObsoleteSPOSites.PS1 from
Office 365 for IT Pros (https://github.com/12Knocksinna/Office365itpros).

Required delegated permissions:
    Sites.Read.All           Read site properties (last activity, storage)
    User.Read.All            Read user/group owner information
    Reports.Read.All         (optional) Read usage report for more accurate activity data

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from datetime import datetime, timezone, timedelta

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_id, test_client_secret, test_tenant


def get_site_owner(site) -> str:
    """Attempt to resolve the owner of a site.

    For group-connected sites, derives ownership from the Microsoft 365
    Group. For classic sites, falls back to site collection admin.
    """
    try:
        if hasattr(site, "group_id") and site.group_id and site.group_id.guid != "00000000-0000-0000-0000-000000000000":
            # Group-connected — owner info would need Graph GroupMember.Read.All
            return f"Group: {site.group_id.guid}"
        admins = site.site_collection_admins.get().execute_query()
        if admins:
            return ", ".join(a.email for a in admins if a.email)
    except Exception:
        pass
    return "Unknown"


def find_inactive_sites(days_threshold: int = 90, include_channel_sites: bool = False) -> list[dict]:
    """Find sites without content modifications within *days_threshold*.

    Args:
        days_threshold: Number of days of inactivity to flag a site.
        include_channel_sites: If True, include Teams private/shared channel sites.

    Returns:
        List of dicts with site URL, title, last activity, storage, owner.
    """
    ctx = ClientContext(test_admin_site_url).with_client_secret(
        test_tenant, test_client_id, test_client_secret
    )
    admin = Tenant(ctx)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_threshold)

    sites = admin.get_site_properties_from_sharepoint().execute_query()
    results = []

    for site in sites:
        # Skip archived sites
        if getattr(site, "archive_status", None) == "NotArchived":
            continue

        # Skip Teams channel sites unless explicitly included
        template = getattr(site, "template", "")
        if not include_channel_sites and template in ("TEAMCHANNEL#0", "TEAMCHANNEL#1"):
            continue

        # Skip redirect sites (placeholders)
        if template == "REDIRECTSITE#0":
            continue

        try:
            # Get site properties with last activity
            site_props = admin.get_site_properties_from_sharepoint_by_url(
                site.url
            ).execute_query()

            last_activity = getattr(site_props, "last_content_modified_date", None)

            if last_activity and last_activity < cutoff:
                results.append({
                    "url": site.url,
                    "title": site.title,
                    "last_activity": last_activity,
                    "template": template,
                    "storage_used_mb": getattr(site, "storage_usage_current", 0),
                    "storage_quota_mb": getattr(site, "storage_quota", 0),
                    "owner": get_site_owner(site),
                })
        except Exception as e:
            print(f"  Skipping {site.url}: {e}")

    return results


def main():
    print("Fetching SharePoint Online sites...")
    inactive = find_inactive_sites(days_threshold=90)

    if not inactive:
        print("No inactive sites found.")
        return

    print(f"\nFound {len(inactive)} sites inactive for 90+ days:\n")
    print(f"{'Site Title':40s} {'URL':50s} {'Last Activity':25s} {'Storage':10s} {'Owner'}")
    print("-" * 140)
    for s in sorted(inactive, key=lambda x: x["last_activity"]):
        storage = f"{s['storage_used_mb']} MB"
        print(
            f"{s['title'][:38]:40s} "
            f"{s['url'][:48]:50s} "
            f"{s['last_activity'].strftime('%Y-%m-%d %H:%M'):25s} "
            f"{storage:10s} "
            f"{s['owner']}"
        )


if __name__ == "__main__":
    main()
