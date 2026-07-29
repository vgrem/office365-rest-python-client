"""
Break permission inheritance on a list (unique permissions).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)
doc_lib = ctx.web.default_document_library()
doc_lib.break_role_inheritance(copy_role_assignments=False, clear_sub_scopes=True).execute_query()
print("Permission inheritance broken on list")
