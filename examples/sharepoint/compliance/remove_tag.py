"""
Remove a compliance tag from a list or list item.

Requires ``Sites.ReadWrite.All`` to read, ``Sites.FullControl.All``
to clear the compliance tag.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/compliance/compliance-tag-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

# Remove compliance tag from a list
target_list = ctx.web.lists.get_by_title("Documents")
target_list.set_compliance_tag("").execute_query()
print("Compliance tag cleared from 'Documents' list.")
