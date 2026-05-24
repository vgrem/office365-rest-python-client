"""
Grant a user permissions on a list or library.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.role_type import RoleType
from tests import test_client_id, test_password, test_site_url, test_tenant, test_user_principal_name, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
doc_lib = ctx.web.default_document_library()
doc_lib.add_role_assignment(test_user_principal_name, RoleType.Contributor).execute_query()
print("Access granted on list")
