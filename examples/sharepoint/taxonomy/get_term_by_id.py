"""
Gets a term by its GUID from the TaxonomyHiddenList.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/taxonomy
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(tenant, client_id, cert_thumbprint, cert_path)
term_guid = "f9a6dae9-633c-474b-b35e-b235cf2b9e73"
taxonomy_list = ctx.web.lists.get_by_title("TaxonomyHiddenList")
result = taxonomy_list.items.first("IdForTerm ne '{0}'".format(term_guid)).get().execute_query()
print(result.properties.get("Title"))
