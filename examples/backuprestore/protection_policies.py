"""
List OneDrive for Business protection policies and their inclusion rules.

Shows what is protected by the Microsoft 365 Backup Storage service.

Requires delegated permission ``BackupRestore-Control.Read.All``.

https://learn.microsoft.com/en-us/graph/api/backuprestoreroot-list-onedriveforbusinessprotectionpolicies
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    policies = client.solutions.backup_restore.one_drive_for_business_protection_policies.get().execute_query()

    print(f"OneDrive protection policies ({len(policies)}):\n")
    for policy in policies:
        props = policy.properties
        rules = policy.drive_inclusion_rules.get().execute_query() if len(policy.drive_inclusion_rules) else []
        rule_count = len(rules) if rules else 0
        print(
            f"  {props.get('displayName', '(unnamed)'):40s}  status={props.get('status', '?')}  drive rules={rule_count}"
        )


if __name__ == "__main__":
    main()
