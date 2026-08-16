"""
Creates an organization-wide sharing link for a folder.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

import json

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

folder_url = "Shared Documents/Archive"
folder = ctx.web.get_folder_by_server_relative_url(folder_url)

result = folder.share_link(SharingLinkKind.OrganizationView).execute_query()
print(json.dumps(result.value.to_json(), indent=4))
print(f"Organization link: {result.value.sharingLinkInfo.Url}")
