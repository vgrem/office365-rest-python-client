# Licensing

Six examples, in the order the questions are asked: what the tenant owns, what one person
holds, whether a call may rely on it, who has what, how to change it, and what the change did
to the plans.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Organization.Read.All` | Read subscribed SKUs and their service plans | [Organization permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#organization-permissions) |
| `User.Read.All` | Read users and their license assignments | [User permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#user-permissions) |
| `User.ReadWrite.All` | Assign and remove licenses | [User permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#user-permissions) |
| `Group.ReadWrite.All` | Assign a license to a group | [Group permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#group-permissions) |

| Example | Writes | Question |
|---|---|---|
| [`inventory.py`](./inventory.py) | — | What does the tenant own — seats, state, how many are left? `--plans` lists the plans inside each SKU |
| [`whose.py`](./whose.py) | — | Who holds this SKU (`--sku`), or what does this person hold (`--user`) with each plan's provisioning status? |
| [`check.py`](./check.py) | — | Is the seat — or the capability inside it — actually held? `--plan RECORDS_MANAGEMENT` |
| [`assign.py`](./assign.py) | ✓ | Add or `--remove` one licence, refusing the calls Graph would refuse: no `usageLocation`, no seat left, already assigned. `--dry-run` stops before the write |
| [`group_license.py`](./group_license.py) | ✓ | Licence a group once and let Graph keep its members licensed |
| [`plans.py`](./plans.py) | ✓ | List the service plans of a SKU, or `--plan-off EXCHANGE_S_ENTERPRISE` for one user |

Every script is runnable and documents itself:

```bash
python inventory.py --help
python assign.py --user ada@contoso.com --sku SPE_E5 --dry-run
```

---

## Two questions, not one

`subscribedSkus` says what the tenant **buys**; `licenseDetails` says what one **seat grants**.
A SKU part number is packaging, a service plan is capability — and a seat may carry a plan no
retail SKU name suggests:

```python
from office365.directory.licenses.tenant import Licences
from office365.graph_client import GraphClient

client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret("client_id", "client_secret")

held = Licences.of_tenant(client)
print(sorted(held.names))  # SKU part numbers and provisioned plan names
print(held.holds("RECORDS_MANAGEMENT"))  # True for DEVELOPERPACK_E5
print([sku.sku_part_number for sku in held.carrying("RECORDS_MANAGEMENT")])
```

Only a plan whose `provisioningStatus` is `Success` counts, and nothing is cached: a grant
changes the answer, and the library is not the level that knows when.

---

## Official docs

- [License management API](https://learn.microsoft.com/en-us/graph/api/resources/license)
- [Subscribed SKU API](https://learn.microsoft.com/en-us/graph/api/resources/subscribedsku)
- [Assign license to a user](https://learn.microsoft.com/en-us/graph/api/user-assignlicense)
- [Assign license to a group](https://learn.microsoft.com/en-us/graph/api/group-assignlicense)
