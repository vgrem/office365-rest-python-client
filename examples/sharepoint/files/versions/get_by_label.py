"""
Retrieves a specific version of a file by version label.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
file_url = "SitePages/Home.aspx"
version = ctx.web.get_file_by_server_relative_path(file_url).versions.get_by_label("1.0").execute_query()

print(version)
