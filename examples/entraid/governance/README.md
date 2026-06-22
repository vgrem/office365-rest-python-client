# Microsoft Entra ID Governance

Examples for Entra ID governance features — terms of use, access
reviews, PIM, entitlement management, and change notifications.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Agreement.Read.All` | Read terms of use agreements and acceptances | [Governance permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#governance-permissions) |
| `AccessReview.Read.All` | List access review definitions and decisions | |
| `RoleManagement.Read.Directory` | Read PIM role assignments | |
| `EntitlementManagement.Read.All` | Read access packages and assignments | |
| `User.Read.All` | Read users for compliance reporting | |

---

## Examples

| Scenario | File | Permission |
|---|---|---|
| Terms of use — list agreements, check acceptances, find pending users | [`terms_of_use.py`](./terms_of_use.py) | `Agreement.Read.All` |
| Access reviews — history definitions, instances, schedule definitions | [`access_reviews.py`](./access_reviews.py) | `AccessReview.Read.All` |
| Access review pending decisions | [`pending_decisions.py`](./pending_decisions.py) | `AccessReview.Read.All` |
| PIM role assignments — who has privileged roles | [`privileged_roles.py`](./privileged_roles.py) | `RoleManagement.Read.Directory` |
| Entitlement management access packages | [`entitlement_packages.py`](./entitlement_packages.py) | `EntitlementManagement.Read.All` |
| Change notifications — create, renew, delete subscriptions | [`change_notifications.py`](./change_notifications.py) | Varies by resource |

---

## Quick start

```python
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    "client_id", "client_secret"
)

agreements = client.identity_governance.terms_of_use.agreements.get().execute_query()
for a in agreements:
    print(a.display_name)
```

---

## Official docs

- [Microsoft Entra ID Governance API](https://learn.microsoft.com/en-us/graph/api/resources/identitygovernance-overview)
- [Access reviews API](https://learn.microsoft.com/en-us/graph/api/resources/accessreviewsv2-overview)
- [Terms of use API](https://learn.microsoft.com/en-us/graph/api/resources/agreement)
- [PIM API](https://learn.microsoft.com/en-us/graph/api/resources/privilegedidentitymanagement-root)
- [Entitlement management API](https://learn.microsoft.com/en-us/graph/api/resources/entitlementmanagement-overview)
- [Change notifications API](https://learn.microsoft.com/en-us/graph/api/resources/webhooks)
