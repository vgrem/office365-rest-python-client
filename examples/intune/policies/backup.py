"""Back up every Intune policy to JSON: the object as the service states it, plus its targets.

A backup that says *what* a policy is but not *who* it reaches cannot restore anything, and
assignments live beside the policy rather than inside it — so both are written, one file per
object, in one directory per family. The files are the policy's own payload, so a restore is a
re-post of ``policy`` and a re-assign of ``assignments``, and a diff between two backups is the
drift that happened in between.

    python backup.py                          # ./intune-backup/<family>/<policy>.json
    python backup.py --out /tmp/tenant-2024-06
    python backup.py --family compliance_policies

Reads the ``beta`` root, because the Settings Catalog family does not exist on v1.0.

Requires delegated ``DeviceManagementConfiguration.Read.All``.

https://learn.microsoft.com/en-us/graph/api/intune-deviceconfig-deviceconfiguration-list
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict

from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion
from office365.runtime.client_request_exception import ClientRequestException
from tests.settings import client_id, password, tenant, username

#: Directory name, navigation property on ``client.device_management``.
FAMILIES = (
    ("device_configurations", "device_configurations"),
    ("compliance_policies", "device_compliance_policies"),
    ("settings_catalog", "configuration_policies"),
)


def file_name(policy) -> str:
    """A git- and filesystem-safe file name, with the id kept so a rename stays a rename."""
    label = re.sub(r"[^A-Za-z0-9._-]+", "-", policy.display_name or "unnamed").strip("-").lower()
    return f"{label or 'unnamed'}-{policy.id}.json"


def document(policy, assignments) -> Dict[str, Any]:
    """One policy, as the service states it, with the assignments that give it meaning."""
    return {
        "@odata.type": policy.entity_type_name,
        "id": policy.id,
        "displayName": policy.display_name,
        "policy": policy.to_json(),
        "assignments": [assignment.to_json() for assignment in assignments],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Back up Intune policies to JSON")
    parser.add_argument("--out", default="intune-backup", help="Directory to write into")
    parser.add_argument("--family", help="Only this family: " + ", ".join(name for name, _ in FAMILIES))
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    client.version = GraphVersion.BETA
    target = Path(args.out)

    written = 0
    for family, navigation in FAMILIES:
        if args.family and args.family != family:
            continue
        try:
            policies = list(getattr(client.device_management, navigation).get_all().execute_query())
        except ClientRequestException as exc:
            print(f"[skipped] {family}: {exc.code}: {exc.message}")
            print("Grant admin consent for DeviceManagementConfiguration.Read.All and re-run.")
            continue

        if not policies:
            print(f"{family}: no policy objects")
            continue
        (target / family).mkdir(parents=True, exist_ok=True)
        for policy in policies:
            assignments = policy.assignments.get().execute_query()
            path = target / family / file_name(policy)
            path.write_text(json.dumps(document(policy, assignments), indent=2, sort_keys=True), encoding="utf-8")
            written += 1
        print(f"{family}: {len(policies)} policy object(s)")

    if not written:
        print(f"Nothing to back up: {target} would be empty.")
        return
    print(f"Wrote {written} file(s) under {target.resolve()}")


if __name__ == "__main__":
    main()
