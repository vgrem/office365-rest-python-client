"""
Report storage usage across all SharePoint Online sites.

Quotas vs actual usage, percentage consumed, and sites approaching
or exceeding their storage limits. Helpful for capacity planning
and identifying sites that need archiving or quota increases.

Inspired by Report-SPOSiteStorageUsage.PS1 and
ReportSPOSiteStorageUsedGraph.PS1 from Office 365 for IT Pros.

Required delegated permissions:
    Sites.Read.All         Read site properties (storage quota, usage)
    User.Read.All          Read site owner information

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_id, test_client_secret, test_tenant

_KB = 1024
_WARNING_PCT = 80
_MAX_PCT = 100


def format_mb(mb_value: int) -> str:
    """Format megabytes into a human-readable size string."""
    if mb_value >= _KB:
        return f"{mb_value / _KB:.1f} GB"
    return f"{mb_value} MB"


def get_site_storage_report(threshold_pct: float = 80.0) -> list[dict]:
    """Report storage usage across all SPO sites.

    Args:
        threshold_pct: Alert threshold — sites above this usage
                       percentage are flagged.

    Returns:
        List of dicts with site storage details, sorted by usage % descending.
    """
    ctx = ClientContext(test_admin_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
    admin = Tenant(ctx)

    sites = admin.get_site_properties_from_sharepoint().execute_query()
    report = []

    for site in sites:
        quota = getattr(site, "storage_quota", 0)
        usage = getattr(site, "storage_usage_current", 0)

        if quota == 0:
            pct = 0.0
        else:
            pct = round((usage / quota) * 100, 1)

        report.append(
            {
                "url": site.url,
                "title": site.title,
                "template": getattr(site, "template", ""),
                "quota_mb": quota,
                "usage_mb": usage,
                "usage_pct": pct,
                "exceeded": usage > quota,
            }
        )

    # Sort by usage percentage descending
    report.sort(key=lambda r: r["usage_pct"], reverse=True)
    return report


def main():
    print("Fetching site storage information...\n")
    report = get_site_storage_report(threshold_pct=80.0)

    # Summary
    total_sites = len(report)
    exceeded = [r for r in report if r["exceeded"]]
    near_limit = [r for r in report if _WARNING_PCT <= r["usage_pct"] < _MAX_PCT]

    print(f"Total sites:         {total_sites}")
    print(f"Exceeding quota:     {len(exceeded)}")
    print(f"Near limit ({_WARNING_PCT}%+):   {len(near_limit)}")
    print()

    if exceeded:
        print("=== Sites exceeding storage quota ===\n")
        for r in exceeded:
            print(f"  {r['title']}")
            print(f"    URL:       {r['url']}")
            print(f"    Used:      {format_mb(r['usage_mb'])}")
            print(f"    Quota:     {format_mb(r['quota_mb'])}")
            print()

    if near_limit:
        print("=== Sites nearing storage limit ===\n")
        print(f"{'Title':40s} {'Used':15s} {'Quota':15s} {'Used %':>8s}")
        print("-" * 80)
        for r in near_limit:
            print(
                f"{r['title'][:38]:40s} "
                f"{format_mb(r['usage_mb']):15s} "
                f"{format_mb(r['quota_mb']):15s} "
                f"{r['usage_pct']:>7.1f}%"
            )


if __name__ == "__main__":
    main()
