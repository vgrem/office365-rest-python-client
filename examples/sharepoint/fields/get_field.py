"""
Get a field (column) by name from a list or web.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(test_tenant, test_client_id, test_username, test_password)
target_list = ctx.web.lists.get_by_title("Documents")
field = target_list.fields.get_by_internal_name_or_title("Title").get().execute_query()
print(f"Field: {field.title}  (type: {field.field_type_kind})")
