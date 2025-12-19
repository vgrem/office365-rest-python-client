from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)


sites = client.sites.get().execute_query()
for site in sites:

    try:
        site.delete_object().execute_query()
        print("✓ Success")
    except ClientRequestException as e:
        print(f"✗ Failed: {str(e)}...")
