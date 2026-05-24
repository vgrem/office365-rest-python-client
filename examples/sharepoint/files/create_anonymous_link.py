"""
Creates and returns an anonymous link that can be used to access a document without needing to authenticate
"""

import datetime
from datetime import timedelta

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_site_url, test_tenant

client = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "Shared Documents/Financial Sample.xlsx"
file = client.web.get_file_by_server_relative_path(file_url)
expires = datetime.datetime.now() + timedelta(minutes=120)
result = file.create_anonymous_link_with_expiration(expires).execute_query()
print(result.value)
