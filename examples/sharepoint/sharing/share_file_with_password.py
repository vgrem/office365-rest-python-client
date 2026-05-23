"""
Shares a file with a password-protected sharing link.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from office365.sharepoint.sharing.role_type import RoleType
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
file_url = "Shared Documents/SharePoint User Guide.docx"
target_file = ctx.web.get_file_by_server_relative_url(file_url)

result = target_file.share_link(SharingLinkKind.Flexible, role=RoleType.Editor, password="password").execute_query()
print("Shared link info: {0}".format(result.value.sharingLinkInfo))
