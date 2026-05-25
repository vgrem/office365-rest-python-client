"""Demonstrates how to export list items to a CSV file

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import csv
import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_tenant, test_username, test_team_site_url

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

# 1.retrieve list data
tasks_list = ctx.web.lists.get_by_title("Company Tasks")
items = tasks_list.items.top(100).get().execute_query()

# 2.export to a file
path = os.path.join(tempfile.mkdtemp(), "Contacts.csv")
with open(path, "w") as fh:
    fields = items[0].properties.keys()
    w = csv.DictWriter(fh, fields)
    w.writeheader()
    for item in items:
        w.writerow(item.properties)
print("List data has been exported into '{0}' file".format(path))
