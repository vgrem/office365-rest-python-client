"""
Retrieves all sub-webs within a site collection.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_site_url

client = ClientContext(test_site_url).with_credentials(test_client_credentials)

webs = client.web.get_all_webs().execute_query()
for web in webs:
    print(web.url)
