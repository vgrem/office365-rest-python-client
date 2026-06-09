"""
Quota management — read and update storage quotas for SharePoint
sites and OneDrive.

Extends the existing site_storage_report.py with quota update
capabilities. This example shows how to:
  - Report storage usage across all sites
  - Update site storage quota
  - Set OneDrive quota for a user
  - Configure default storage quota for new site creation

Requires delegated permission ``Sites.FullControl.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/tenant/SetSiteProperties
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_id, test_client_secret, test_tenant

_WARNING_PCT = 80
_MAX_PCT = 100

_KB = 1024


def format_mb(mb_value: int) -> str:
    if mb_value >= _KB:
        return f"{mb_value / _KB:.1f} GB"
    return f"{mb_value} MB"


def main():
    ctx = ClientContext(test_admin_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
    tenant = Tenant(ctx)

    # -- Step 1: report storage usage across all sites --
    print("Fetching site storage info... (this may take a moment)\n")
    sites = tenant.get_site_properties_from_sharepoint().execute_query()

    report = []
    for site in sites:
        quota = getattr(site, "storage_quota", 0) or 0
        usage = getattr(site, "storage_usage_current", 0) or 0
        pct = round((usage / quota) * 100, 1) if quota > 0 else 0
        report.append(
            {
                "url": site.url,
                "title": site.title,
                "quota_mb": quota,
                "usage_mb": usage,
                "usage_pct": pct,
                "site": site,
            }
        )

    report.sort(key=lambda r: r["usage_pct"], reverse=True)

    total = len(report)
    exceeded = [r for r in report if r["usage_mb"] > r["quota_mb"]]
    near_limit = [r for r in report if _WARNING_PCT <= r["usage_pct"] < _MAX_PCT]

    print(f"Total sites: {total}")
    print(f"Exceeding quota: {len(exceeded)}")
    print(f"Nearing limit ({_WARNING_PCT}%+): {len(near_limit)}\n")

    if near_limit:
        print(f"{'Title':40s} {'Used':15s} {'Quota':15s} {'Used %':>8s}")
        print("-" * 80)
        for r in near_limit[:10]:
            print(
                f"{r['title'][:38]:40s} "
                f"{format_mb(r['usage_mb']):15s} "
                f"{format_mb(r['quota_mb']):15s} "
                f"{r['usage_pct']:>7.1f}%"
            )
        print()

    # -- Step 2: update storage quota for a site near limit --
    if near_limit:
        target = near_limit[0]
        print(f"Updating quota for: {target['title']}")
        print(f"  Current quota: {format_mb(target['quota_mb'])}")
        new_quota = target["quota_mb"] + (5 * _KB)  # +5 GB
        print(f"  New quota:     {format_mb(new_quota)}")

        # Update the site properties to set new quota
        target["site"].set_property("StorageMaximumLevel", new_quota)
        target["site"].set_property("StorageWarningLevel", int(new_quota * 0.8))
        target["site"].update_ex().execute_query()
        print("  ✓ Quota updated.")

        # Verify
        updated_site = tenant.get_site_properties_from_sharepoint().execute_query()
        for s in updated_site:
            if s.url == target["url"]:
                print(f"  Verified: quota = {format_mb(getattr(s, 'storage_quota', 0))}")

    # -- Step 3: read current OneDrive default storage quota --
    one_drive_quota = tenant.one_drive_storage_quota
    print(f"\nDefault OneDrive storage quota: {format_mb(one_drive_quota) if one_drive_quota else '(not set)'}")

    # -- Step 4: update OneDrive quota (commented) --
    # tenant.set_property("OneDriveStorageQuota", 1024 * 100)  # 100 GB
    # tenant.update().execute_query()
    # print("✓ OneDrive default quota updated to 100 GB.")

    # -- Step 5: set OneDrive quota for a specific user (commented) --
    # from office365.sharepoint.userprofiles.people_manager import PeopleManager
    # pm = PeopleManager(ctx)
    # pm.set_user_onedrive_quota("user@contoso.com", new_quota_mb=1024 * 100, new_quota_warning_mb=1024 * 80)\
    #     .execute_query()
    # print("✓ User OneDrive quota updated.")


if __name__ == "__main__":
    main()
