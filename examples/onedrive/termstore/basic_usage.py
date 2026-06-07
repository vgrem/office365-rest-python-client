"""
Export and import taxonomy (term store) groups, sets, and terms.

The term store is a managed metadata service for consistent
tagging across SharePoint and OneDrive.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/termstore-list-groups
https://learn.microsoft.com/en-us/graph/api/termstore-group-post-sets
https://learn.microsoft.com/en-us/graph/api/termstore-set-post-children
"""

import uuid

from office365.graph_client import GraphClient
from tests import (
    test_client_id,
    test_client_secret,
    test_root_site_url,
    test_tenant,
)

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

store = client.sites.get_by_url(test_root_site_url).term_store

# 1. List existing groups
groups = store.groups.get().execute_query()
print(f"Term store groups ({len(groups)}):")
for g in groups:
    print(f"  {g.display_name}")

# 2. Create a group
group_name = f"SDK_{uuid.uuid4().hex[:8]}"
group = store.groups.add(group_name).execute_query()
print(f"\nGroup created: {group.display_name}")

# 3. Create a set with terms
set_name = "Project Tags"
term_set = group.sets.add(set_name).execute_query()
print(f"  Set: {term_set.display_name}")

# 4. Add terms to the set
for term_name in ["Urgent", "In Progress", "Completed"]:
    term = term_set.children.add(label=term_name).execute_query()
    print(f"    Term: {term.display_name}")
