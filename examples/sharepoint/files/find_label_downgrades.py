"""
List the tenant's Microsoft Purview sensitivity labels.

Shows each label's id, display name, priority, and enabled state —
useful for planning label baselines before applying them to sites/files.

Note: detecting label *downgrades* requires the audit log search API
(``/security/auditLog/queries``), which is not modeled by this SDK.

Requires delegated permission ``SecurityDataGovernance.Read.All`` (or
Purview compliance admin).

https://learn.microsoft.com/en-us/graph/api/resources/sensitivitylabel
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="List sensitivity labels")
    parser.add_argument("--top", type=int, default=100, help="maximum number of labels (default 100)")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    labels = client.security.data_security_and_governance.sensitivity_labels.top(args.top).get().execute_query()

    print(f"Sensitivity labels ({len(labels)}):")
    for label in sorted(labels, key=lambda label: label.priority or 0):
        state = "enabled" if label.enabled else "disabled"
        print(f"  {label.display_name or label.name or '?':35s} priority={label.priority}  {state}  ({label.id})")


if __name__ == "__main__":
    main()
