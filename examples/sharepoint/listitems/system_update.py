"""Demonstrates how to update system metadata properties of a list item

Note: When using Entra ID (formerly Azure AD), some system metadata updates
(e.g. Author, Editor) require Sites.FullControl permission.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import sys
from datetime import datetime, timedelta

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.user_value import FieldUserValue
from tests import (
    test_client_credentials,
    test_site_url,
    test_user_principal_name,
)

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

target_list = ctx.web.lists.get_by_title("Documents")
items = target_list.items.get().top(1).execute_query()
if len(items) == 0:
    sys.exit("No items were found")

assert items[0].id is not None
# item_to_update = items[0]
item_to_update = items.get_by_id(items[0].id)


author = ctx.web.site_users.get_by_email(test_user_principal_name)


created_date = datetime.utcnow() - timedelta(days=21)
modified_date = datetime.utcnow() - timedelta(days=14)
result = item_to_update.validate_update_list_item(
    {
        "Editor": FieldUserValue.from_user(author),
        # "Modified": modified_date,
        # "Created": created_date,
        "Author": FieldUserValue.from_user(author),
    },
    # dates_in_utc=True,
    new_document_update=True,
).execute_query()

has_any_error = any([getattr(item, "HasException", False) for item in result.value])
if has_any_error:
    print("Item update completed with errors, for details refer 'ErrorMessage' property")
else:
    print("Item has been updated successfully")
