"""
Prints server settings
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.server_settings import ServerSettings
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(test_tenant, test_client_id, test_username, test_password)
is_online = ServerSettings.is_sharepoint_online(ctx)
blocked_file_extensions = ServerSettings.get_blocked_file_extensions(ctx)
installed_languages = ServerSettings.get_global_installed_languages(ctx, 15)
ctx.execute_batch()
print(f"Is SharePoint Online? : {is_online.value}")
print(f"Installed languages : {installed_languages}")
