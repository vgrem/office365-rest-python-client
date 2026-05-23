"""
Reset permission inheritance on a list (revert to parent permissions).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
doc_lib = ctx.web.default_document_library()
doc_lib.reset_role_inheritance().execute_query()
print("Permission inheritance reset on list")
