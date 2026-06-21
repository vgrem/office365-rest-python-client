"""
Remove a compliance tag from a list or list item.

Requires ``Sites.ReadWrite.All`` to read, ``Sites.FullControl.All``
to clear the compliance tag.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/compliance/compliance-tag-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant

ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)

# Remove compliance tag from a list
target_list = ctx.web.lists.get_by_title("Documents")
target_list.set_compliance_tag(tag_id="").execute_query()
print("Compliance tag cleared from 'Documents' list.")
