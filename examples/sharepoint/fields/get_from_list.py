"""Demonstrates how to retrieve all fields from a SharePoint list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/field
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

client = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
target_list = client.web.lists.get_by_title("Site Pages")
fields = target_list.fields.get().execute_query()
for field in fields:
    print(f"Field name {field.internal_name}")
