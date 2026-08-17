"""
Prints SharePoint server settings including SharePoint Online status and installed languages.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/server-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.server_settings import ServerSettings
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
is_online = ServerSettings.is_sharepoint_online(ctx)
blocked_file_extensions = ServerSettings.get_blocked_file_extensions(ctx)
installed_languages = ServerSettings.get_global_installed_languages(ctx, 15)
ctx.execute_batch()
print(f"Is SharePoint Online? : {is_online.value}")
print(f"Installed languages : {installed_languages}")
