"""
Audit: export the full OneNote notebook hierarchy — notebooks,
section groups, sections, and pages — with metadata.

Walks every notebook and recursively resolves section groups.
Useful for content discovery, inventory, and data mapping.

Requires delegated permission ``Notes.Read``.

https://learn.microsoft.com/en-us/graph/api/onenote-list-notebooks
https://learn.microsoft.com/en-us/graph/api/onenote-list-sectiongroups
https://learn.microsoft.com/en-us/graph/api/onenote-list-sections
https://learn.microsoft.com/en-us/graph/api/onenote-list-pages
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

notebooks = client.me.onenote.notebooks.get().execute_query()

print(f"Found {len(notebooks)} notebooks\n")

for nb in notebooks:
    print(f"📓 {nb.display_name}  (id: {nb.id})")
    if nb.is_default:
        print("   (default notebook)")

    section_groups = nb.section_groups.get().execute_query()
    for sg in section_groups:
        print(f"  📁 Section group: {sg.display_name}")
        # Recursively get sections in this section group
        sections = sg.sections.get().execute_query()
        for s in sections:
            pages = s.pages.top(5).select(["title", "createdDateTime", "lastModifiedDateTime"]).get().execute_query()
            print(f"    📄 {s.display_name}  ({len(pages)} pages)")
            for p in pages:
                title = p.properties.get("title", "(untitled)")
                modified = p.properties.get("lastModifiedDateTime", "")
                print(f"       • {title}  [{modified}]")
            if len(pages) == 0:
                print("       (empty)")

    # Top-level sections (not inside section groups)
    sections = nb.sections.get().execute_query()
    for s in sections:
        pages = s.pages.top(5).select(["title", "lastModifiedDateTime"]).get().execute_query()
        print(f"  📄 {s.display_name}  ({len(pages)} pages)")
        for p in pages:
            title = p.properties.get("title", "(untitled)")
            modified = p.properties.get("lastModifiedDateTime", "")
            print(f"     • {title}  [{modified}]")
        if len(pages) == 0:
            print("     (empty)")

    print()
