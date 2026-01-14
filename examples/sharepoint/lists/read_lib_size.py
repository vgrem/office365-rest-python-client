from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
lib = ctx.web.lists.get_by_title("Documents").root_folder.expand(["StorageMetrics"]).get().execute_query()
print(f"List size (in bytes): {lib.storage_metrics.total_size}")
