# Directory (Microsoft Entra ID)

Examples for working with Microsoft Entra ID — users, groups, service
principals, conditional access, and PIM role assignments.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `User.Read.All` | Read user profiles and directory objects | [User permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#user-permissions) |
| `Group.Read.All` | Read group membership and properties | [Group permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#group-permissions) |
| `Policy.Read.All` | Read conditional access policies | [Policy permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#policy-permissions) |
| `Application.Read.All` | Read service principals and apps | [Application permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#application-permissions) |
| `RoleManagement.Read.All` | Read PIM role assignments | [Role management permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#role-management-permissions) |

---

## Patterns

| Category | Scenario | File |
|---|---|---|
| **Users** | User sign-in status, unlicensed accounts | [`users/report.py`](./users/report.py) |
| **Groups** | Group ownership, members, orphans | [`groups/manage.py`](./groups/manage.py) |
| **Service principals** | List apps and delegated permissions | [`service_principals/report.py`](./service_principals/report.py) |
| **Conditional access** | List CA policies | [`conditional_access/report.py`](./conditional_access/report.py) |
| **PIM** | Privileged role assignments | [`pim/report.py`](./pim/report.py) |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

users = client.users.top(10).get().execute_query()
for u in users:
    print(f"{u.display_name}  ({u.user_principal_name})")
```

---

## Official docs

- [Microsoft Entra ID](https://learn.microsoft.com/en-us/entra/identity)
- [Graph API for users](https://learn.microsoft.com/en-us/graph/api/resources/user)
- [Graph API for groups](https://learn.microsoft.com/en-us/graph/api/resources/group)
- [Conditional access API](https://learn.microsoft.com/en-us/graph/api/resources/conditionalaccesspolicy)
