"""
Exports tenant settings to a CSV file in the Style Library.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_admin_credentials, test_admin_site_url

admin_client = ClientContext(test_admin_site_url).with_credentials(test_admin_credentials)
result = admin_client.tenant.export_to_csv(view_xml="<View/>", list_name="Style Library").execute_query()
print("Sites details have been exported into {0}{1}".format(test_admin_site_url, result.value))
