"""Demonstrates how to retrieve all fields from a SharePoint site

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/field
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

client = ClientContext(test_team_site_url).with_credentials(test_client_credentials)

web_fields = client.web.fields.get().execute_query()
for f in web_fields:
    print(f"Field name {f.internal_name}")
