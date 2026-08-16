"""Demonstrates how to save a list as a template in the list template gallery

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
ctx.web.lists.get_by_title("Site Pages").save_as_template("SitePages.stp", "Site Pages", "", True).execute_query()
