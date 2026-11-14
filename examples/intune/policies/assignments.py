"""Who does a policy reach? The group side of every assignment, in one report.

An assignment row names a *target*, not a group: the target is one of several shapes under
one name — all devices, all users, a group, an exclusion group — and only a group target
carries a ``groupId``. So "who gets this" is read from the target that has an id, and the id
is resolved to a name once here rather than left as a GUID in the output.

    python assignments.py                        # every policy, grouped by family
    python assignments.py --unassigned            # what nobody receives
    python assignments.py --group "All Windows"   # what reaches one group

The Settings Catalog family is beta-only, so the client addresses ``beta``: an Intune report that
mixes modern and classic policy objects has no single v1.0 answer.

Requires delegated ``DeviceManagementConfiguration.Read.All`` and ``Directory.Read.All`` (to name
the groups an assignment targets).

https://learn.microsoft.com/en-us/graph/api/intune-deviceconfig-deviceconfigurationassignment-list
https://learn.microsoft.com/en-us/graph/api/resources/deviceandappmanagementassignmenttarget
"""

from __future__ import annotations

import argparse
from typing import Dict, List, Tuple

from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (
    DeviceAndAppManagementAssignmentTarget,
)
from office365.graph_client import GraphClient
from office365.graph_version import GraphVersion
from office365.runtime.client_request_exception import ClientRequestException
from tests.settings import client_id, password, tenant, username

#: Family name in the report, navigation property on ``client.device_management``.
FAMILIES = (
    ("device configurations", "device_configurations"),
    ("compliance policies", "device_compliance_policies"),
    ("settings catalog", "configuration_policies"),
)


def describe(target: DeviceAndAppManagementAssignmentTarget, names: Dict[str, str]) -> str:
    """What one assignment aims at, with the group id resolved when it is one."""
    if not target.group_id:
        return "all devices and users"
    label = names.get(target.group_id, target.group_id)
    if target.device_and_app_management_assignment_filter_id:
        return f"group {label} (filter {target.device_and_app_management_assignment_filter_id})"
    return f"group {label}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Which policies reach whom")
    parser.add_argument("--unassigned", action="store_true", help="Only policies nobody receives")
    parser.add_argument("--group", help="Only the policies that reach this group display name")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    client.version = GraphVersion.BETA
    wanted_group = client.groups.find_by_name(args.group).execute_query().id if args.group else None

    #: (family, policy, targets) - read first, so every group id is known before it is named.
    rows: List[Tuple[str, object, List[DeviceAndAppManagementAssignmentTarget]]] = []
    for family, navigation in FAMILIES:
        try:
            policies = list(getattr(client.device_management, navigation).get_all().execute_query())
            for policy in policies:
                targets = [assignment.target for assignment in policy.assignments.get().execute_query()]
                rows.append((family, policy, targets))
        except ClientRequestException as exc:
            print(f"[skipped] {family}: {exc.code}: {exc.message}")
            print("Grant admin consent for DeviceManagementConfiguration.Read.All and re-run.")

    group_ids = sorted({target.group_id for _, _, targets in rows for target in targets if target.group_id})
    names = (
        {group.id: group.display_name for group in client.directory_objects.get_by_ids(group_ids).execute_query()}
        if group_ids
        else {}
    )

    def selected(entry: Tuple[str, object, List[DeviceAndAppManagementAssignmentTarget]]) -> bool:
        targets = entry[2]
        if args.unassigned:
            return not targets
        return wanted_group is None or any(target.group_id == wanted_group for target in targets)

    if not rows:
        print("No Intune policy objects in this tenant: nothing is assigned yet.")
        return

    for family, _ in FAMILIES:
        entries = [entry for entry in rows if entry[0] == family and selected(entry)]
        if not entries:
            continue
        print(f"\n{family} ({len(entries)}):")
        for _, policy, targets in entries:
            print(f"  {policy.display_name or '(unnamed)':45s} {len(targets)} target(s)")
            for target in targets:
                print(f"    {describe(target, names)}")

    if not args.unassigned:
        silent = [entry for entry in rows if not entry[2]]
        hint = " - run --unassigned to list" if silent else ""
        print(f"\n{len(silent)} of {len(rows)} policies reach nobody{hint}")


if __name__ == "__main__":
    main()
