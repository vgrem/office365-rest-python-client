"""Expands a SharePoint group into a collection of principal information objects.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)

result = ctx.web.associated_member_group.expand_to_principals(100).execute_query()
for principal_info in result.value:
    print(principal_info)
