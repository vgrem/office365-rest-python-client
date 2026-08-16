"""Demonstrates how to retrieve list items using OData filter queries

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import datetime

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
list_title = "Site Pages"
site_pages = ctx.web.lists.get_by_title(list_title)
from_datetime = datetime.datetime(2022, 1, 20, 0, 0)
filter_text = f"Created gt datetime'{from_datetime.isoformat()}'"
include_fields = ["Created", "EncodedAbsUrl"]
items = site_pages.items.filter(filter_text).select(include_fields).get().execute_query()
print(f"Loaded items count: {len(items)}")
for item in items:
    print(item.properties["EncodedAbsUrl"])
