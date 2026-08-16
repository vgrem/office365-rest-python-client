"""
Shares a file with a password-protected sharing link.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from office365.sharepoint.sharing.role_type import RoleType
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
file_url = "Shared Documents/SharePoint User Guide.docx"
target_file = ctx.web.get_file_by_server_relative_url(file_url)

result = target_file.share_link(
    SharingLinkKind.Flexible, role=RoleType.Editor.value, password="password"
).execute_query()
print("Shared link info: {0}".format(result.value.sharingLinkInfo))
