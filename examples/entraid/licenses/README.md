# Licensing

Six examples, in the order the questions are asked: what the tenant owns, what one person
holds, whether a call may rely on it, who has what, how to change it, and what the change did
to the plans. Two more carry that state as a list: `export_licences.py` writes it,
`import_licences.py` plans every row before sending one.

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
| [`export_licences.py`](./export_licences.py) | — | Every user's SKUs and disabled plans as CSV — the input the next script reads |
| [`import_licences.py`](./import_licences.py) | ✓ | Set each user to what a row asks, printing `already held`, `blocked — …` or the change it makes. `--dry-run` stops at the plan |

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

## A list, both ways

`export_licences.py > licences.csv` writes the state; `import_licences.py licences.csv --dry-run`
answers what the other tenant would need. Graph's own preconditions are decided before a row is
sent, and a licence a group grants is reported rather than removed — the group owns it. For a
population, group-based licensing is the way round; a per-user fan-out is for a one-off list.

## Official docs

- [License management API](https://learn.microsoft.com/en-us/graph/api/resources/license)
- [Subscribed SKU API](https://learn.microsoft.com/en-us/graph/api/resources/subscribedsku)
- [Assign license to a user](https://learn.microsoft.com/en-us/graph/api/user-assignlicense)
- [Assign license to a group](https://learn.microsoft.com/en-us/graph/api/group-assignlicense)
