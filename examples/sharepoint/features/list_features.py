"""Demonstrates how to list activated features on a site.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/features
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_site_url

ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)

features = ctx.site.features.get().execute_query()
for f in features:
    print(f"  {f.display_name or 'N/A'}  (ID: {f.definition_id})")
print(f"Total: {len(features)} activated features")
