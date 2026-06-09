"""
Export SharePoint sites to CSV — site inventory for migration
planning and tenant management.

Exports all SharePoint Online sites with URL, title, template,
owner, storage usage/quota, compatibility level, hub association,
and last content modified date.

Essential for:
  - SharePoint migration planning (source inventory)
  - Tenant consolidation or split
  - Storage governance and legacy site identification

Requires delegated permission ``Sites.Read.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/tenant/GetSitePropertiesFromSharePoint
"""

import csv
import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_id, test_client_secret, test_tenant

OUTPUT_FILE = "/tmp/sharepoint_sites_export.csv"
_KB = 1024


def format_mb(mb_value: int) -> str:
    if mb_value >= _KB:
        return f"{mb_value / _KB:.1f} GB"
    return f"{mb_value} MB"


def main():
    ctx = ClientContext(test_admin_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
    tenant = Tenant(ctx)

    print("Fetching SharePoint sites...")
    sites = tenant.get_site_properties_from_sharepoint().execute_query()
    print(f"  Found {len(sites)} sites\n")

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "url", "title", "template", "owner", "storageQuotaMB",
            "storageUsageMB", "storageUsagePct", "compatibilityLevel",
            "sharingCapability", "lockState", "lastContentModifiedDate",
            "hubSite", "createdDate", "websCount",
        ])

        for site in sites:
            url = getattr(site, "url", "?")
            title = getattr(site, "title", "(untitled)")
            template = getattr(site, "template", "?")
            owner = getattr(site, "owner_login_name", "?") or getattr(site, "owner", "?")
            quota = getattr(site, "storage_quota", 0) or 0
            usage = getattr(site, "storage_usage_current", 0) or 0
            pct = round((usage / quota) * 100, 1) if quota > 0 else 0
            compat = getattr(site, "compatibility_level", "?")
            sharing = getattr(site, "sharing_capability", "?")
            lock = getattr(site, "lock_state", "")
            last_mod = getattr(site, "last_content_modified_date", "")
            if hasattr(last_mod, "strftime"):
                last_mod = last_mod.strftime("%Y-%m-%d")
            created = getattr(site, "created_time", "")
            if hasattr(created, "strftime"):
                created = created.strftime("%Y-%m-%d")
            is_hub = getattr(site, "is_hub_site", False)
            webs = getattr(site, "webs_count", "?")

            writer.writerow([url, title, template, owner, quota, usage, pct, compat, sharing, lock, last_mod, is_hub, created, webs])
            print(f"  {title[:40]:40s}  {format_mb(usage):>10s} / {format_mb(quota):>10s}  ({pct}%)")

    print(f"\n✓ Exported {len(sites)} sites to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
