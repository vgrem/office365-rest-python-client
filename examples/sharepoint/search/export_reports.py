"""
Export SharePoint search reports for a tenant.

Checks the search admin endpoint first, then exports the requested report.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

REPORT_TYPES = [
    "ReportTopQueries",
    "ReportNumberOfQueries",
    "ReportAbandonedQueries",
    "ReportNoResult",
    "ReportQueryRules",
]


def main():
    parser = argparse.ArgumentParser(description="Export SharePoint search reports")
    parser.add_argument("--tenant-id", required=True, help="Tenant id (GUID) to export reports for")
    parser.add_argument("--report-type", choices=REPORT_TYPES, default="ReportTopQueries", help="Report type")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    ping = ctx.search_setting.ping_admin_endpoint().execute_query()
    if not ping.value:
        raise SystemExit("Search admin endpoint is not reachable")

    result = ctx.search_setting.export_search_reports(
        tenant_id=args.tenant_id, report_type=args.report_type
    ).execute_query()
    print(f"Exported '{args.report_type}' report")
    print(result.value)


if __name__ == "__main__":
    main()
