"""
Retrieves folder system metadata.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
list_title = "Documents"

folder_items = (
    ctx.web.lists.get_by_title(list_title)
    .items.filter("FSObjType eq 1")
    .select(
        [
            "FSObjType",
            "Author/Id",
            "Author/Title",
            "Author/Name",
            "Editor/Id",
            "Editor/Title",
            "Editor/Name",
        ]
    )
    .expand(["Author", "Editor"])
    .get()
    .execute_query()
)

folder_path = "Archive"  # folder relative path
folder_item = (
    ctx.web.lists.get_by_title(list_title)
    .get_item_by_url(folder_path)
    .select(
        [
            "Author/Id",
            "Author/Title",
            "Author/Name",
            "Editor/Id",
            "Editor/Title",
            "Editor/Name",
        ]
    )
    .expand(["Author", "Editor"])
    .get()
    .execute_query()
)

print(folder_item.properties.get("Author"))
print(folder_item.properties.get("Editor"))
