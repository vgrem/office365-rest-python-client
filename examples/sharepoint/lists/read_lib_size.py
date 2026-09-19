"""Demonstrates how to retrieve the storage size of a SharePoint document library

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
lib = ctx.web.lists.get_by_title("Stocks_5yr_Large").expand(["RootFolder/StorageMetrics"]).get().execute_query()
print(f"List size (in bytes): {lib.root_folder.storage_metrics.total_size}")
print(f"Items count: {lib.item_count}")
