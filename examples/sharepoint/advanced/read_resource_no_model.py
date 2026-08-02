"""
Demonstrates how to construct and submit requests without a model involved.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

import json

from office365.sharepoint.request import SharePointRequest
from tests.settings import client_id, password, site_url, tenant, username

request = SharePointRequest(site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)

try:
    response = request.execute_request("web/currentUser")
    parsed = json.loads(response.content)
    prop_val = parsed["d"]["UserPrincipalName"]
    print(f"UserPrincipalName: {prop_val}")
except Exception as e:
    print(f"An error occurred: {e}")
