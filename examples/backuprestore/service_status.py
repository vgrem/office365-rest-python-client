"""
Check the Microsoft 365 Backup Storage service status.

Requires delegated or application permission ``BackupRestore-Control.Read.All``
and an active Microsoft 365 Backup Storage license (checked upfront via
``require_license``).

https://learn.microsoft.com/en-us/graph/api/backuprestoreroot-list-servicestatus
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret).require_license("BACKUP")
    backup = client.solutions.backup_restore
    backup.get().execute_query()
    status = backup.service_status

    print("Microsoft 365 Backup Storage service status:")
    print(f"  Status:            {status.status}")
    print(f"  Consumer:          {status.backupServiceConsumer}")
    print(f"  Disable reason:    {status.disableReason}")
    print(f"  Grace period till: {status.gracePeriodDateTime or '?'}")
    print(f"  Restore allowed:   {status.restoreAllowedTillDateTime or '?'}")


if __name__ == "__main__":
    main()
