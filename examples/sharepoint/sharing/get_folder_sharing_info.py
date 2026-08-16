"""
Gets the sharing information for a folder.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharing-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

folder_url = "Shared Documents/Archive"
result = ctx.web.get_folder_by_server_relative_url(folder_url).get_sharing_information().execute_query()

for sharing_link in result.sharing_links:
    print(sharing_link)
