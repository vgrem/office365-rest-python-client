"""
Connect to SharePoint using ACS App-Only principal (client credentials).

⚠️ DEPRECATED: Azure Access Control Service (ACS) is being retired.
ACS stopped working for new tenants on Nov 1, 2024, and will be fully
retired on April 2, 2026. Use Azure AD certificate auth instead.

This method is still relevant for SharePoint on-premises.

See https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azureacs
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_site_url

ctx = ClientContext(test_site_url).with_client_credentials(test_client_id, test_client_secret)
target_web = ctx.web.get().execute_query()
print(target_web.url)
