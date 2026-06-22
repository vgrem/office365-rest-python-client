"""Filter list items using OData filter expressions."""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(
    tenant=tenant, client_id=client_id, username=username, password=password
)
items = ctx.web.lists.get_by_title("Documents").items.get().filter("FSObjType eq 0").execute_query()
for item in items:
    print(item.properties)
