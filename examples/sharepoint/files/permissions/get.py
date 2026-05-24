"""
Retrieves the permissions on the file that are assigned to the current user.
"""

from pprint import pprint

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "Shared Documents/big_buck_bunny.mp4"
file = ctx.web.get_file_by_server_relative_url(file_url)
file_item = file.listItemAllFields.select(["EffectiveBasePermissions"]).get().execute_query()
pprint(file_item.effective_base_permissions.permission_levels)
