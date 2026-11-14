# Policies

The **configure** stage. Intune delivers two kinds of policy to devices:

- **Compliance policies** decide whether a device *may* access corporate
  resources (PIN, encryption, OS version, jailbreak). Conditional access reads
  this verdict.
- **Configuration profiles** push *settings* — Wi-Fi, VPN, certificates,
  restrictions — regardless of compliance.

```mermaid
flowchart LR
    G["Entra group"] -->|assigned to| CP["device_compliance_policies"]
    G -->|assigned to| CF["device_configurations"]
    CP --> S["device_status_overview"]
    CF --> S
    S --> R["reports/ + devices/compliance.py"]
```

## Start here

```bash
python compliance_policies.py --details
python configuration_profiles.py --details
python assignments.py --unassigned
python backup.py --out /tmp/tenant-backup
```

| Script | What / why | Permissions |
|---|---|---|
| [`compliance_policies.py`](./compliance_policies.py) | Every compliance policy with version and, with `--details`, its assignment count and deployment status. | `DeviceManagementConfiguration.Read.All` |
| [`configuration_profiles.py`](./configuration_profiles.py) | Every configuration profile with assignment/status rollup. | `DeviceManagementConfiguration.Read.All` |
| [`assignments.py`](./assignments.py) | Who a policy reaches: every family's targets with the group **named**, and `--unassigned` for the policies nobody gets. `--group "All Windows"` inverts the question. | `DeviceManagementConfiguration.Read.All`, `Directory.Read.All` |
| [`backup.py`](./backup.py) | Every policy and its assignments as one JSON file per object, one directory per family — the input a restore re-posts and a diff shows drift against. | `DeviceManagementConfiguration.Read.All` |

## How assignment works

Policies are **assigned to groups**, not devices. An assignment is a
`DeviceAndAppManagementAssignmentTarget` — one name for several shapes: all devices, all
users, a group, an exclusion group. Only a group target carries a `groupId`, so which target
a policy reaches is read from that, and `assignments.py` resolves the id to a name in one
`getByIds` call rather than leaving a GUID in the output.
Once a device receives a policy, its outcome is visible via
`device_status_overview` (success/failed/error/pending) and, per device, via
`devices/compliance.py`.

- **Creating/editing** a policy means `device_compliance_policies.add(...)` or
  `.get()...update()`; assigning is a separate `assign` action. This folder
  focuses on reading, which is the safe, common task.

## Beta, because Settings Catalog is beta-only

`configurationPolicies` — the Settings Catalog family, which is most of modern Intune — is
declared by the beta service root alone, and a v1.0 client raises `NotSupportedInVersion`
rather than quietly answering half the fleet. So these reports address beta:

```python
client.version = GraphVersion.BETA
```

`backup.py` and `assignments.py` do this before the first read; the classic families answer
identically from either root, which is why one client covers both.

## Official docs

- [List compliance policies](https://learn.microsoft.com/en-us/graph/api/intune-devices-devicecompliancepolicy-list)
- [List configuration profiles](https://learn.microsoft.com/en-us/graph/api/intune-deviceconfig-deviceconfiguration-list)
- [Assign a policy](https://learn.microsoft.com/en-us/graph/api/intune-devices-devicecompliancepolicy-assign)
