"""
Gets basic properties of a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

client = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
site = client.site.get().execute_query()
print("Site url: {}".format(site.url))

result = site.is_valid_home_site().execute_query()
print("Is home site: {}".format(result.value))
