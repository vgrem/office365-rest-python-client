"""
Enable the Microsoft 365 Backup Storage service for the tenant.

The ``enable`` API requires a **multi-tenant** app registered in another
tenant that holds the Backup Storage permission; pass its tenant id as
``--app-owner-tenant-id``.

Requires delegated permission ``BackupRestore-Control.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/backuprestoreroot-enable
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Enable Microsoft 365 Backup Storage")
    parser.add_argument("--app-owner-tenant-id", required=True, help="Tenant id of the multi-tenant app owner")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    result = client.solutions.backup_restore.enable(args.app_owner_tenant_id).execute_query()

    print("Backup Storage enable request submitted:")
    print(f"  Status:  {result.value.status}")
    print(f"  Consumer: {result.value.backupServiceConsumer}")


if __name__ == "__main__":
    main()
