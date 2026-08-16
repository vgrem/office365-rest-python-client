# Microsoft Intune

Examples for working with Microsoft Intune via the Graph API —
managed device inventory, remote actions, hardware, primary-user management,
apps, VPP tokens, app-protection (MAM) policies, audit, and reporting.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `DeviceManagementManagedDevices.Read.All` | List and read managed devices | [Intune permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#device-management-permissions) |
| `DeviceManagementManagedDevices.PrivilegedOperations.All` | Wipe, retire, sync devices, manage primary user | [Intune permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#device-management-permissions) |
| `DeviceManagementServiceConfig.Read.All` | Read device management settings, audit events, categories | [Intune permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#device-management-permissions) |
| `DeviceManagementConfiguration.Read.All` | Read device configuration and compliance policies | [Intune permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#device-management-permissions) |
| `DeviceManagementApps.Read.All` | Read mobile apps, VPP tokens, app-protection policies | [Intune permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#device-management-permissions) |

Admin consent is required for all Intune permissions.

---

## How Intune works

```mermaid
flowchart LR
    A[Intune tenant] --> B[Managed devices]
    A --> C[Compliance policies]
    A --> D[Configuration profiles]
    B --> E[Remote actions: wipe / retire / sync]
    E --> F[Audit events track every action]
    A --> G[Reports: activity & enrollment]
```

Intune manages devices, enforces compliance, and tracks all
admin actions via audit events.

---

## Patterns

| Category | Scenario | File | Permission |
|---|---|---|---|
| **Device management** | Enriched device inventory with compliance state, OS, last sync | [`managed_devices/inventory.py`](./managed_devices/inventory.py) | `DeviceManagementManagedDevices.Read.All` |
| **Device management** | Hardware inventory: OS, manufacturer, model, storage, enrollment | [`managed_devices/hardware.py`](./managed_devices/hardware.py) | `DeviceManagementManagedDevices.Read.All` |
| **Device management** | Primary user: read/assign/remove, set ownership | [`managed_devices/primary_user.py`](./managed_devices/primary_user.py) | `DeviceManagementManagedDevices.Read.All` + `PrivilegedOperations.All` |
| **Device management** | Remote actions: wipe (factory reset), retire (remove company data), force sync | [`managed_devices/remote_actions.py`](./managed_devices/remote_actions.py) | `DeviceManagementManagedDevices.PrivilegedOperations.All` |
| **Applications** | Mobile apps inventory by publisher and publishing state | [`applications/mobile_apps.py`](./applications/mobile_apps.py) | `DeviceManagementApps.Read.All` |
| **Applications** | Apple VPP tokens and sync/expiry status | [`applications/vpp_tokens.py`](./applications/vpp_tokens.py) | `DeviceManagementApps.Read.All` |
| **Policies** | App Protection (MAM) policies and managed app registrations | [`policies/managed_app_policies.py`](./policies/managed_app_policies.py) | `DeviceManagementApps.Read.All` |
| **Audit** | List audit events (admin action trail) and device categories | [`audit/device_audit.py`](./audit/device_audit.py) | `DeviceManagementServiceConfig.Read.All` |
| **Reporting** | Device configuration activity and enrollment failure reports | [`reports/device_activity.py`](./reports/device_activity.py) | `DeviceManagementConfiguration.Read.All` |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

devices = client.device_management.managed_devices.get().execute_query()
for d in devices:
    print(f"{d.device_name:35s}  [{d.compliance_state}]")
```

---

## Official docs

- [Microsoft Intune](https://learn.microsoft.com/en-us/mem/intune)
- [Intune Graph API overview](https://learn.microsoft.com/en-us/graph/api/resources/intune-graph-overview)
- [Intune permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#device-management-permissions)
