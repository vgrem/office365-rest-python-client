"""
Returns a folder object from a tokenized sharing link URL.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

folder = ctx.web.get_folder_by_server_relative_url("Shared Documents/Archive")
# Share a folder
result = folder.share_link(SharingLinkKind.OrganizationView).execute_query()


shared_folder = ctx.web.get_folder_by_guest_url(str(result.value)).execute_query()
print(shared_folder)
