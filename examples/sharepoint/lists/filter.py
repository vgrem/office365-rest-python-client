"""Demonstrates how to apply OData filtering to a list collection

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
result = ctx.web.lists.get().select(["IsSystemList", "Title"]).filter("IsSystemList eq false").execute_query()
for lst in result:
    print(lst.title)
