"""
Remove a user from site collection administrators.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_user_principal_name, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
user = ctx.web.ensure_user(test_user_principal_name).execute_query()
# ctx.site.remove_site_collection_administrator(user).execute_query()
print(f"Admin removed: {test_user_principal_name}")
