# 0005 — The seat a licence is checked against

Status: **implemented** (`office365/permissions/declaration.py`, `office365/licensing/guard.py`).
Extends `0004-licences-on-the-type.md`, which declares *which* plan carries a capability. This one
answers *whose* it has to be, because a licence question has two answers and only one of them was
being asked.

## 1. Two facts, two reads

`subscribedSkus` answering yes means the tenant bought the plan for somebody. It never means the
identity making the call holds one: a kiosk account, a guest, a service account, and an app-only
token are all inside the same tenant and none of them is the person the licence was bought for.
The other fact is `/me/licenseDetails`, and it is a different read with a different answer.

So the failure modes are different too, and a refusal that names only the plan points at the wrong
one. Twenty of `ManagedDevice`'s members say `INTUNE_A` today; "the tenant's subscriptions carry
none of them" is true and useless when the tenant bought four hundred seats and the caller has
none. The seat is therefore part of the declaration, not an argument somebody passes at the call
site.

## 2. The word: `seat=`

`ServicePlanInfo.appliesTo` is `"User"` or `"Company"` for every plan Microsoft reports
(`office365/directory/licenses/service_plan_info.py:23`), and `_provisioned_plans` already filters
on exactly those two strings. The service's own word for the distinction is therefore *seat*, and
`TENANT` / `USER` are its two values:

```python
TENANT = "tenant"  # bought: subscribedSkus answers it
USER = "user"  # assigned: /me/licenseDetails answers it
SEATS = (TENANT, USER)
```

`scope=` was the alternative and is the wrong word: `scopes=` already means OAuth in this tree
(`grep -rn "scopes=" --include=*.py office365 | wc -l` → `13`), and one vocabulary for one fact is
the rule that also made licences be named by plan rather than by SKU. Before this change the word
`seat` appeared once in `office365/permissions` and `office365/licensing` — in a comment. It is now
the keyword.

## 3. The surface

| What | Where | Shape |
| --- | --- | --- |
| the two values | `declaration.py` | `TENANT`, `USER`, `SEATS` |
| the fact | `declaration.py` | `@dataclass(frozen=True) class Licence: plans: tuple[str, ...]; seat: str = TENANT` |
| the marker | `declaration.py` | `@requires_license(*plans, seat=TENANT)` — one decorator, one keyword |
| the read | `declaration.py` | `licence_of(target) -> Optional[Licence]` |
| the plans alone | `declaration.py` | `licenses_of(target)` — unchanged, delegates to `licence_of` |
| the fold | `declaration.py` | `with_licences(declaration, licence: Optional[Licence])` |
| where the seat lands | `declaration.py` | `PermissionRequirement.seat: str = TENANT` |
| how it reads | `declaration.py` | `seat_suffix(seat)` → `", assigned to you"` or `""` |
| the second reader | `guard.py` | `LicenceGuard(read, read_user=None, mode=OFF, ttl=...)` |
| the second fact | `guard.py` | `held_by_user`, cached under its own `_user_read_at` |
| the refusal | `guard.py` | `LicenceRequired(plans, target, seat=TENANT)` |
| the client's two lambdas | `graph_client.py` | `licence_guard` |

Three decisions hold the shape still:

* **A keyword, not a second decorator.** `@requires_user_license(...)` would have forked the
  reading side — `licenses_of`, `licence_of`, `with_licences`, `Capabilities.licenses`, the fold in
  `_tag_query` and `_declarations_of`, and the CLI page would each need a branch. One decorator
  with one keyword keeps a single reading path.
* **The fold carries the seat even when the member narrows the plans.** A plan answers *which*
  capability and the seat answers *whose*, and the second never varies by verb. A PIM activation is
  a person's seat whichever request object carries it.
* **The seat lives on `PermissionRequirement`, never on `Requirement`.** `Requirement` is the
  grant-shaped object (`unmet`, `shortfall`, bypass roles, the matrix, `tests/preflight.py`); a seat
  is not a grant and nothing in that path moves.

## 4. What the guard does, in order

`check(target, plans=None, seat=None)` — `seat=None` asks the type, so a caller holding a marked
type never has to know which question it stands for.

1. `off` returns immediately; the tenant is not read. `check_query` reads the seat off the
   declaration it already reads, so `GraphRequest` keeps the signature it had.
2. The **tenant** is asked first, even when the seat is `USER`: a plan nobody bought cannot be
   assigned to anybody, so the cheaper and more certain fact settles it, with the sentence that
   names the real cause.
3. `USER` then asks `held_by_user`. Holding any one of the named plans is enough.

| tenant holds | seat asked | `enforce` | `warn` |
| --- | --- | --- | --- |
| none of them | not reached | raises, "the tenant's subscriptions carry none of them" | warns once |
| one of them | `read_user` None | **passes**, one note: no user reader | same |
| one of them | read raises | **passes**, one note: unreadable | same |
| one of them | holds none | raises, "your assignments carry none of them" | warns once |
| one of them | holds one | passes, silently | passes |
| unreadable | not reached | passes, one note | same |

The `read_user is None` row is the one to defend, and it is the app-only row: an app acts for users
but its token names none, so there is no `/me` to read. Unknown never blocks — a guard that refuses
a call it could not check is a worse failure than the 403 it was explaining — and the note says
*which* unknown it is, so nobody grants `User.Read` expecting the message to change.

## 5. What flipped, and what deliberately did not

**One marker:**

```python
@requires_license("AAD_PREMIUM_P2", seat=USER)
class PrivilegedAccessScheduleRequest(Request):
```

`grep -rn "seat=USER" --include=*.py office365 | wc -l` → `1`. PIM activation is the one case here
where the licensed identity genuinely is the one calling: an eligibility schedule request is
created *by* the person activating, and the plan is assigned to them.

**Nothing else flipped.** Intune is 66 of the 78 stamps and stays `TENANT`
(`grep -rn "^@requires_license" --include=*.py office365 | wc -l` → `78`): the seat Intune requires
belongs to the *device's* user, not the caller's, which is a third question — `subject=` — needing a
lookup per device per call. The service's own 403 answers that one better than a guess. Access
reviews and access packages stay `TENANT`: the plan is bought for the tenant's governance features,
not for the reviewer.

## 6. Reading it

`to_hint()` and `describe()` say the seat only when it is the caller's:

```
one of the licences AAD_PREMIUM_P2, assigned to you.
Licenses: AAD_PREMIUM_P2, assigned to you
```

A `TENANT` licence reads exactly as it did in `0004`, so nothing that already printed a licence
changed. The CLI page says it once, above the actions:

`office365/cli.py` — `_page` appends ` (assigned to you)` to `needs a licence: …`.

## 7. Where the code is

| What | Where |
| --- | --- |
| `TENANT`, `USER`, `SEATS`, `Licence`, `seat_suffix` | `office365/permissions/declaration.py` |
| `requires_license(..., seat=)`, `licence_of`, `with_licences` | `office365/permissions/declaration.py` |
| the exported names | `office365/permissions/__init__.py` |
| `held_by_user`, `check(..., seat=)` | `office365/licensing/guard.py` |
| `LicenceRequired(..., seat=)` and its two sentences | `office365/licensing/guard.py` |
| the two readers handed over | `office365/graph_client.py` — `licence_guard` |
| the fold, both call sites | `office365/permissions/declaration.py` (`_tag_query`), `office365/capabilities.py` (`_declarations_of`) |
| the page line | `office365/cli.py` — `_page` |

Tests: `tests/unit/test_licence_guard.py` — `python -m pytest tests/unit/test_licence_guard.py -q`
→ `15 passed`. Four of them are this document's claims: the caller's assignments are what decides a
user seat, holding one of them is enough, a tenant that bought none is refused before a seat is
asked about, and an app-only caller is noted once rather than refused.
