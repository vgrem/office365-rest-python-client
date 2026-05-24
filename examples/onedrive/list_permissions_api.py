"""
Demonstrates @require_permission and verify_permissions diagnostic.

Usage:
    python -m examples.onedrive.list_permissions_api
"""

from office365.directory.permissions.checker import verify_permissions
from office365.graph_client import GraphClient
from office365.onedrive.drives.collection import DriveCollection
from tests import test_client_id, test_client_secret, test_tenant

client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

report = verify_permissions(client, DriveCollection.get)
print(report)
