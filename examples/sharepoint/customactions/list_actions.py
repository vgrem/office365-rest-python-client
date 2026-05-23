"""
List all custom actions on a site (web) or list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/rest-user-custom-action
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

# Site-scoped custom actions
actions = ctx.web.user_custom_actions.get().execute_query()
print(f"=== Site actions ({len(actions)}) ===")
for a in actions:
    print(f"  {a.properties.get('Title', '')}  (ID: {a.properties.get('Id', '')})")

# List-scoped custom actions
target_list = ctx.web.lists.get_by_title("Documents")
list_actions = target_list.user_custom_actions.get().execute_query()
print(f"=== List actions on 'Documents' ({len(list_actions)}) ===")
for a in list_actions:
    print(f"  {a.properties.get('Title', '')}  (ID: {a.properties.get('Id', '')})")
