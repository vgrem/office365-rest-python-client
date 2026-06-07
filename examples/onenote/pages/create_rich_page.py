"""
Create a rich OneNote page with tables, bullet lists, numbered lists,
embedded images, and styled text — all inline as input HTML.

The page is created in the first available section of the default
notebook.

Requires delegated permission ``Notes.ReadWrite``.

https://learn.microsoft.com/en-us/graph/onenote-create-page
https://learn.microsoft.com/en-us/graph/onenote-input-output-html
"""

import sys
from io import BytesIO

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

sections = client.me.onenote.sections.top(1).get().execute_query()
if len(sections) == 0:
    sys.exit("No sections found. Create a notebook first.")

html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Project Status — June 2026</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; }
        h1 { color: #0078d4; }
        .status-done { background: #dff6dd; padding: 2px 8px; border-radius: 4px; }
        .status-wip { background: #fff3ce; padding: 2px 8px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Project Status</h1>
    <p>Generated via <strong>Microsoft Graph API</strong> on <em>June 2026</em>.</p>

    <h2>Team</h2>
    <ul>
        <li><b>Alice</b> — Engineering lead</li>
        <li><b>Bob</b> — Product manager</li>
        <li><b>Carol</b> — Designer</li>
    </ul>

    <h2>Milestones</h2>
    <ol>
        <li>Design review <span class="status-done">Done</span></li>
        <li>API integration <span class="status-wip">In progress</span></li>
        <li>User testing</li>
    </ol>

    <h2>Budget allocation</h2>
    <table>
        <thead>
            <tr><th>Category</th><th>Budget</th><th>Spent</th></tr>
        </thead>
        <tbody>
            <tr><td>Engineering</td><td>$50,000</td><td>$32,000</td></tr>
            <tr><td>Design</td><td>$15,000</td><td>$8,500</td></tr>
            <tr><td>Operations</td><td>$10,000</td><td>$9,200</td></tr>
        </tbody>
    </table>

    <p><img src="https://via.placeholder.com/600x200/0078d4/ffffff?text=Dashboard+Preview"
            alt="Project dashboard" width="600" /></p>

    <p>Last updated: <i>2026-06-07</i></p>
</body>
</html>"""

section = sections[0]
page = section.pages.add(presentation_file=BytesIO(html_content.encode("utf-8"))).execute_query()
print(f"Page created: {page.title}")
print(f"Web URL: {page.links.oneNoteWebUrl}")
