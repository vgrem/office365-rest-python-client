"""
Creates a tokenized organization sharing link for a file.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
file = ctx.web.get_file_by_server_relative_url("Shared Documents/Financial Sample.xlsx")
result = file.share_link(SharingLinkKind.OrganizationView).execute_query()
print("Shared link url: {0}".format(result.value.sharingLinkInfo))
