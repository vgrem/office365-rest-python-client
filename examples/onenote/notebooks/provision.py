"""
Provision a new OneNote notebook with a standard set of sections
and an initial page in each.

Demonstrates the "notebook from template" pattern — useful for
onboarding, training, or project standardization.

Requires delegated permission ``Notes.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/onenote-post-notebooks
"""

from office365.graph_client import GraphClient
from tests import (
    create_unique_name,
    test_client_id,
    test_password,
    test_tenant,
    test_username,
)

SECTION_TEMPLATE = [
    {"title": "Meeting Notes", "page": "<p>Weekly team sync notes go here.</p>"},
    {"title": "Project Plan", "page": "<p>Timeline, milestones, and deliverables.</p>"},
    {"title": "Decisions", "page": "<p>Architectural and design decisions with rationale.</p>"},
    {"title": "Resources", "page": "<p>Links to relevant docs, tools, and references.</p>"},
]

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

notebook_name = create_unique_name("Project")
notebook = client.me.onenote.notebooks.add(notebook_name).execute_query()
print(f"Notebook created: {notebook.display_name}")

for spec in SECTION_TEMPLATE:
    section = notebook.sections.add(displayName=spec["title"]).execute_query()
    print(f"  Section: {spec['title']}")

    page_html = f"""<!DOCTYPE html>
<html><head><title>{spec["title"]}</title></head>
<body>{spec["page"]}</body></html>"""

    page = section.pages.add(presentation_file=page_html.encode()).execute_query()
    print(f"    Page: {page.title}")

print(f"\nDone. Notebook URL: {notebook.links.oneNoteWebUrl}")
