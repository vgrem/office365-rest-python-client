"""Gets site basic properties"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

client = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
site = client.site.get().execute_query()
print(f"Site url: {site.url}")

result = site.is_valid_home_site().execute_query()
print(f"Is home site: {result.value}")
