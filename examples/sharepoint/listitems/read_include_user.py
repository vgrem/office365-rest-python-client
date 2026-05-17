"""Demonstrates how to retrieve list items and include user field values (Author, Editor)

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
tasks_list = ctx.web.lists.get_by_title("Company Tasks")
items = (
    tasks_list.items.get()
    .select(["*", "Author/Id", "Author/Title", "Editor/Title"])
    .expand(["Author", "Editor"])
    .execute_query()
)
for item in items:
    author = item.properties.get("Author") or {}
    print("{0}".format(author.get("Title")))
