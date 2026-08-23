"""
Export SharePoint sites to CSV — site inventory for migration
planning and tenant management.

Exports all SharePoint Online sites with URL, title, template, owner,
storage usage/quota, compatibility level, hub association, and dates.
Storage usage percentage is a derived column — compute it in your
spreadsheet (``StorageUsageCurrent / StorageQuota * 100``).

Essential for:
  - SharePoint migration planning (source inventory)
  - Tenant consolidation or split
  - Storage governance and legacy site identification

Requires an app with ``Sites.FullControl.All`` (or a SharePoint /
Global admin account) on the admin site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/tenant/GetSitePropertiesFromSharePoint
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, tenant

COLUMNS = [
    "Url",
    "Title",
    "Template",
    "OwnerLoginName",
    "StorageQuota",
    "StorageUsageCurrent",
    "CompatibilityLevel",
    "SharingCapability",
    "LockState",
    "LastContentModifiedDate",
    "IsHubSite",
    "CreatedTime",
    "WebsCount",
]
_KB = 1024


def format_mb(mb_value: int) -> str:
    if mb_value >= _KB:
        return f"{mb_value / _KB:.1f} GB"
    return f"{mb_value} MB"


def main():
    parser = argparse.ArgumentParser(description="Export SharePoint sites to CSV")
    parser.add_argument("--output", default="/tmp/sharepoint_sites_export.csv", help="output CSV file")
    args = parser.parse_args()

    client = ClientContext(admin_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    admin = Tenant(client)

    # Deferred: load sites, then write the CSV after execute_query().
    with open(args.output, "w", newline="") as f:
        sites = admin.get_site_properties_from_sharepoint().select(COLUMNS).to_csv(f).execute_query()

    print(f"✓ Exported {len(sites)} sites to {args.output}\n")
    for site in sites:
        title = site.get_property("Title") or "(untitled)"
        usage = site.get_property("StorageUsageCurrent") or 0
        quota = site.get_property("StorageQuota") or 0
        pct = round((usage / quota) * 100, 1) if quota > 0 else 0
        print(f"  {title[:40]:40s}  {format_mb(usage):>10s} / {format_mb(quota):>10s}  ({pct}%)")


if __name__ == "__main__":
    main()
