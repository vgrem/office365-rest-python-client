"""
Rename a file or folder by updating its name property.

Requires delegated permission ``Files.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/driveitem-update?view=graph-rest-1.0
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant, test_user_principal_name_alt

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

drive = client.users.get_by_principal_name(test_user_principal_name_alt).drive
item = drive.root.get_by_path("report.docx").get().execute_query()
item.set_property("name", "report_renamed.docx").update().execute_query()
print(f"File renamed to: {item.name}")
