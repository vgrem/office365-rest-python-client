"""
Retrieves basic file properties
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_team_site_url, test_client_id, test_client_secret

ctx = ClientContext(test_team_site_url).with_client_credentials(test_client_id,test_client_secret)
file_url = "SitePages/Home.aspx"
file = ctx.web.get_file_by_server_relative_url(file_url).get().execute_query()

print("File size: ", file.length)
print("File name: ", file.name)
print("File url: ", file.server_relative_url)
