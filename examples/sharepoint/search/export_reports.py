"""
Exports SharePoint search reports for a tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/general-development/sharepoint-search-rest-api-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
result = ctx.search_setting.ping_admin_endpoint().execute_query()
if result.value:
    result = ctx.search_setting.export_search_reports(
        tenant_id="af6a80a4-8b4b-4879-88af-42ff8a545211", report_type="ReportTopQueries"
    ).execute_query()
    print(result)
