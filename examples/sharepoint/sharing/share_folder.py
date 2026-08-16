"""
Demonstrates how to create and retrieve a tokenized sharing link for a folder.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
folder = ctx.web.get_folder_by_server_relative_url("Shared Documents/Archive")

# Share a folder
result = folder.share_link(SharingLinkKind.AnonymousView).execute_query()

# Optional step: resolve folder by guest url
guest_url = result.value.sharingLinkInfo.Url
if guest_url is None:
    raise SystemExit("Failed to create a sharing link")
shared_folder = ctx.web.get_folder_by_guest_url(guest_url).execute_query()
print(shared_folder)
