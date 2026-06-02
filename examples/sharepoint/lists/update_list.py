"""
Update a list's properties (title, description).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
target_list = ctx.web.lists.get_by_title("Documents")
target_list.set_property("Title", "Updated Documents").update().execute_query()
print("List updated")
