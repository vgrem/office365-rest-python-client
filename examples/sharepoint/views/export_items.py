"""
Exports list view items to a CSV file.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
list_title = "Documents"
view_title = "All Documents"
list_view = ctx.web.lists.get_by_title(list_title).views.get_by_title(view_title)
export_path = os.path.join(tempfile.mkdtemp(), f"{view_title}.csv")

with open(export_path, "w", newline="", encoding="utf-8") as f:
    list_view.get_items().to_csv(f).execute_query()

print(f"List view has been exported into '{export_path}' file")
