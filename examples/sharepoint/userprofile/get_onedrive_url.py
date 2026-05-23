"""Gets the OneDrive (default document library) URL for a user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
me = ctx.web.current_user
result = ctx.people_manager.get_default_document_library(me).execute_query()
print(f"OneDrive URL: {result.value}")
