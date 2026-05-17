"""
Demonstrates creating an anonymous sharing link for a file.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests import test_team_site_url, test_user_credentials

ctx = ClientContext(test_team_site_url).with_credentials(test_user_credentials)

remote_file = ctx.web.get_file_by_server_relative_url("Shared Documents/Financial Sample.xlsx")
result = remote_file.share_link(SharingLinkKind.AnonymousView).execute_query()
print(result.value)
