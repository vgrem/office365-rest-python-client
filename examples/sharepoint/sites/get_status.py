"""
Gets the status of a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_admin_credentials, test_admin_site_url, test_team_site_url

admin_client = ClientContext(test_admin_site_url).with_credentials(test_admin_credentials)
result = admin_client.site_manager.get_status(test_team_site_url).execute_query()
print(result.value)
