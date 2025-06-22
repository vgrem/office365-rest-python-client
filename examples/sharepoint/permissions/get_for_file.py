"""
Returns the user permissions for the file.
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
file_url = "SitePages/Home.aspx"
file = ctx.web.get_file_by_server_relative_url(file_url)
result = file.get_user_effective_permissions(
    ctx.web.current_user
).execute_query()
print(result.value)
