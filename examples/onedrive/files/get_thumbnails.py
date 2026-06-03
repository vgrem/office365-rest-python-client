"""
Get the thumbnail set for a drive item.

Requires delegated permission ``Files.Read.All``.

https://learn.microsoft.com/en-us/graph/api/driveitem-list-thumbnails?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant, test_user_principal_name_alt

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

drive = client.users.get_by_principal_name(test_user_principal_name_alt).drive
thumbnails = drive.root.get_by_path("report.docx").thumbnails.get().execute_query()
for t in thumbnails:
    print(f"Small: {t.small.url}")
    print(f"Medium: {t.medium.url}")
    print(f"Large: {t.large.url}")
