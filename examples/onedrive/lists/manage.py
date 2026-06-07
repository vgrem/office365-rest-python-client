"""
Create a SharePoint list with items and custom columns.

Shows how to provision a list, add columns, and create items.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/list-create
https://learn.microsoft.com/en-us/graph/api/listitem-create
https://learn.microsoft.com/en-us/graph/api/columndefinition-create
"""

from office365.graph_client import GraphClient
from office365.onedrive.lists.template_type import ListTemplateType
from tests import (
    create_unique_name,
    test_client_id,
    test_client_secret,
    test_tenant,
)

client = GraphClient(tenant=test_tenant).with_client_secret(
    test_client_id, test_client_secret
)

# 1. Create a document library
list_name = create_unique_name("ProjectAssets")
lib = client.sites.root.lists.add(list_name, ListTemplateType.documentLibrary).execute_query()
print(f"List created: {lib.display_name}")

# 2. Add a text column
col = lib.columns.add_text("Category").execute_query()
print(f"  Column: {col.display_name}")

# 3. Create an item with custom column value
item = lib.items.add(Title="Q4 Report", Category="Finance").execute_query()
print(f"  Item: {item.display_name} (id: {item.id})")

# 4. Read items back
items = lib.items.get().execute_query()
print(f"\nItems in '{lib.display_name}': {len(items)}")
