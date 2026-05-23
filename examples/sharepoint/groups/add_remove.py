"""Demonstrates how to add and remove a site group.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name, test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
group_name = create_unique_name("Group")
group = ctx.web.site_groups.add(group_name).execute_query()
# clean up temporary resources
group.delete_object().execute_query()
