from office365.sharepoint.client_context import ClientContext
from tests import (
    test_client_id,
    test_password,
    test_site_url,
    test_tenant,
    test_username,
)

ctx = ClientContext(test_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
me = ctx.web.current_user.get().execute_query()
print(me.login_name)
