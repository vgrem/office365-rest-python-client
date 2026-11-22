# 0004 — A licence is a fact about a capability, so the type states it

As built. Every number here was taken from this tree with the command printed beside it; the
number is not an estimate, and re-running the command is the way to check that this note still
describes the code.

## 1. What was already declared, and what read it

The model has declared licences for a long time. `office365/permissions/declaration.py` carries
`licenses` on `PermissionRequirement`, `Requirement.groups()` reports it as a group,
`Capabilities.licenses` unions it, and `hints_of()` has a sentence for it. What it did *not* have
was a way to say "this family is licensed" without repeating the licence on every verb, and one
consumer — the command line — read none of it.

The command that showed the second half missing, run against the commit before this work:

```
$ git grep -n hints db04fd9e2 -- office365/cli.py
(no output)
```

So `o365 <noun> -h` printed the flags and nothing about what the service would answer, even for a
command whose declaration already named a permission. That is the cheapest half of the work: the
sentences existed, the page did not ask for them.

The command that showed the first half missing — a licence named by zero types:

```
$ grep -rn "licenses=\[" office365 --include=*.py
office365/search/entity.py:49:        licenses=["SPE_E5"],
```

One call site, and it is the *wrong kind* of one: a licence that belongs to a family, written on
a single method because there was nowhere else to write it. (It is gone now; §5 is what happened
to it.)

## 2. The marker

`@requires_license(...)` sits above the class:

```python
#: What it takes: a conditional access policy exists only where Entra ID P1 does.
@limit(*IDENTITY_PROTECTION_QUOTAS)
@requires_license("AAD_PREMIUM")
class ConditionalAccessPolicy(PolicyDeletableItem):
```

Read back with `licenses_of(target)`, which answers for a type, for a subclass (attribute lookup
walks the MRO, so the nearest declaration wins), and for a member whose qualified name names the
class that stamped it. A member that states nothing about licences on its own declares nothing —
`UnifiedRoleAssignment` is a role *grant*, which needs no PIM, and sits beside
`UnifiedRoleScheduleBase`, which is PIM and does — the two live side by side in
`rolemanagement/unifiedrole/`, and the difference is one marker.

An empty marker is refused at import time rather than at read time:

```
$ .venv/bin/python -c "from office365.permissions.declaration import requires_license; requires_license()"
ValueError: requires_license names no plan: pass at least one service plan, e.g. requires_license('AAD_PREMIUM')
```

## 3. The join — one licence, every verb

A type's licence is one fact. Restating it on 20 verbs is 20 places to forget it, so
`Capabilities.declarations` folds it in: a declaration that names no licence of its own is
replaced with a copy carrying the type's, and one that names its own keeps it. That is how a
single call states "narrower than my family" without a second vocabulary.

`Capabilities.licenses` is then the **union** of the two sources, not the nearest one: a family
with a basic licence and one P2-only verb needs both, and a caller reading the union is told the
whole of what must be bought.

```
$ .venv/bin/python -c "
from office365.capabilities import capabilities_of
from office365.intune.devices.management.managed.device import ManagedDevice
caps = capabilities_of(ManagedDevice)
print(len(caps.declarations), 'declarations')
print({n: d.licenses for n, d in caps.declarations.items() if n in caps.verbs})"
20 declarations
{'locate_device': ('INTUNE_A',), 'wipe': ('INTUNE_A',), 'retire': ('INTUNE_A',), ...}
```

Before the fold every entry was `()`; after it, the 18 that are also commands all read
`('INTUNE_A',)` — one mark above the class reaches the whole family.

## 4. What the command line now says

Two places, both fed by the same two functions:

```
$ o365 graph directory conditional-access-policy
directory conditional-access-policy — ConditionalAccessPolicy
  needs a licence: AAD_PREMIUM

READ
  get      read this one back
```

```
$ o365 graph directory conditional-access-policy get -h
...
Declares no permission.
Needs one of these licences: AAD_PREMIUM.
```

and where a permission *is* declared, the licence joins that sentence instead of repeating it:

```
$ o365 graph directory risky-user dismiss -h
...
This API declares: application IdentityRiskyUser.ReadWrite.All; delegated
IdentityRiskyUser.ReadWrite.All; one of the licences AAD_PREMIUM_P2.
```

The rule is one sentence per fact: `hints_of` adds its own licence line only when the
declaration's line does not already name exactly those plans. A caller who needs the answer as
data asks `capabilities_of`, which has had `licenses` all along.

Both are read off the model, so no page can claim a licence the type does not declare, and a
type that names none prints no line — `o365 sharepoint web` is unchanged.

## 5. The vocabulary, and the two ratchets that keep it

A licence is named by **service plan**, the vocabulary a tenant's `subscribedSkus` already
carries, and the one `Capabilities.licenses` documents. A SKU part number is packaging: the same
capability arrives inside several SKUs and one SKU turns on dozens of plans, so a requirement
written in plans can be checked against any tenant.

`declaration.py` used to call the field "SKU part numbers"; that docstring is now the paragraph
above. The ambiguity had left one declaration spelled the other way:

```
$ grep -rn "licenses=\[" office365 --include=*.py   # before the ratchet existed
office365/search/entity.py:49:        licenses=["SPE_E5"],
```

`SPE_E5` is the SKU, and `LicenceGuard.held` is `LicencesReport.plans` - plan names only - so no
tenant ever reported the part number as a plan: under `enforce` that marker refused every search.
The fix was not a better spelling. `/search/query` has no licence of its own, because what it can
reach depends on the entity types asked for, so the claim was deleted and the note beside it now
carries the whole fact:

```
$ o365 search entity query -h
...
This API declares: application Mail.Read, ...; delegated Mail.Read, ..., Chat.Read. (Permissions
depend on the entity types being queried)
```

Two ratchets keep the vocabulary, and both fail the *test*, never the call:

| Ratchet | What it asserts | Test |
| --- | --- | --- |
| the published list | every plan a marker spells is in `tests/data/service_plans.txt`, the `Service_Plan_Name` column of Microsoft's licensing CSV, refreshed by `python scripts/fetch_service_plans.py` | `test_a_licence_names_a_plan_the_service_publishes` |
| the census | a declaring type in a family that sells a capability names a plan, or is recorded in `SILENT` with the reason it cannot | `test_a_paid_family_says_which_licence_carries_it` |

The census is what found three types §6 had missed. The two PIM schedule requests and the
risky-user collection declare a permission of their own and inherit no stamp - `UnifiedRoleScheduleBase`
is a sibling of the requests, not their base - so they name `AAD_PREMIUM_P2` now. Which families are
compared is itself a decision, written down as `PAID`: a capability that is sold is claimed, and the
free tree (`sharepoint`, `onedrive`, `teams`, ...) is not.

Both read the tree with `ast`, so a marker in a class nobody imports is still checked, and a plan
name built from a variable is refused instead of passing unread:

```
$ .venv/bin/python -m pytest tests/unit/test_permissions.py -q
5 passed
```

The other half of the same decision: `graph_client.require_license()` matches either spelling by
substring. It is the legacy reader; `Capabilities.licenses` and the CLI do not use it.

## 6. What was stamped

A stamp is a claim about licensing that a person has to be able to defend, so each row below is one
judgement about one family, not a copy of a neighbour:

| Family | Plan | Why it is not a permission |
| --- | --- | --- |
| `ConditionalAccessPolicy` | `AAD_PREMIUM` | P1 is what makes the feature exist; no grant creates it on a P1-less tenant |
| `RiskyUser` | `AAD_PREMIUM_P2` | identity protection is P2 |
| `UnifiedRoleScheduleBase` | `AAD_PREMIUM_P2` | a *schedule* is PIM, and PIM is P2 |
| `UnifiedRoleAssignmentScheduleRequest`, `UnifiedRoleEligibilityScheduleRequest` | `AAD_PREMIUM_P2` | activating or making a role eligible is PIM; the tenant holds the plan, so the claim is `TENANT` - an administrator may create one for someone else |
| `RiskyUserCollection` | `AAD_PREMIUM_P2` | dismissing or confirming a risk is its own type, so the entity's stamp does not reach it |
| `PrivilegedAccessScheduleRequest` + its two requests | `AAD_PREMIUM_P2` | PIM for groups is the same product as PIM for roles |
| `AccessReviewInstance`, `AccessReviewStage`, `AccessReviewHistoryInstance` | `AAD_PREMIUM_P2` | access reviews are a P2 feature |
| access packages — `AccessPackage`, its assignment, its request, its resource, its upload session | `AAD_PREMIUM_P2` | entitlement management is P2 |
| 66 Intune types | `INTUNE_A` | a managed device, a policy, a report is Intune; the seat is what a tenant buys |

Conditional Access is `AAD_PREMIUM`, not `_P2`: a P1-only tenant can create a policy, and a marker
that refused it would be wrong about the product. P2 buys risk and PIM, which is why the others say
so.

**A family stamps the root that owns the declarations, not the directory.** Intune is 907 files and
847 classes; 66 of those classes carry a `@require_permission`, 160 of them written in those files
and 165 reached once inheritance is counted, so marking the 781 classes that declare nothing would
say nothing. Where two types share a base, one marker speaks for both:
`licenses_of(PrivilegedAccessGroupAssignmentScheduleRequest)` answers `('AAD_PREMIUM_P2',)` without
that file naming a plan.

Measured, not estimated:

```
$ grep -rn '^@requires_license' --include=*.py office365 | wc -l
81
$ python -  # sum len(capabilities_of(c).declarations) over the stamped classes
types: 81  declarations reached: 188
{'AAD_PREMIUM_P2': [14, 23], 'AAD_PREMIUM': [1, 0], 'INTUNE_A': [66, 165]}
```

`AAD_PREMIUM` reaches 0 declarations because `ConditionalAccessPolicy` declares no permission of
its own: the page and `-h` still say `needs a licence: AAD_PREMIUM`, and a `403` from it has no
declaration to attach the seat to. That is the shape of a type-only stamp, and it is why a denial
hint is not the only place a licence has to be readable.

Three surfaces now say it, all off the same two functions:

```
$ o365 graph intune device-management reports
intune device-management reports — DeviceManagementReports
  needs a licence: INTUNE_A
...
$ o365 graph intune device-management reports get-cached-report -h
... one of the licences INTUNE_A.
$ python -c "GraphClient(tenant=...); c.device_management.managed_devices['abc'].retire(); \
             print(c.last_query.permission_requirement.to_hint())"
... one of the licences INTUNE_A.
```

## 7. What is deliberately not stamped

Three areas hold a plan this tenant has, but the *split inside the area* is a licensing judgement
and one marker would be wrong for half of it. They stay unmarked rather than guessed:

* `directory/synchronization` — cloud sync is P1, on-premises provisioning is free, and both live
  under the same 50 files.
* `security/labels` — a sensitivity label is E3; records and retention are `RECORDS_MANAGEMENT`,
  which is a separate add-on.
* `directory/rolemanagement` — a PIM schedule is P2 (`schedule_base.py` says so); role *definitions*
  and plain assignments are free.

Five families need a plan this tenant does not hold, so the name is unverifiable here: lifecycle
workflows (Governance), eDiscovery, Copilot, Teams Premium, and `backuprestore`. Stamping them now
would make a typo indistinguishable from "not bought" — the failure mode §5 exists to avoid.

`security/threatintelligence` and `security/attacksimulations` stay unstamped for a different
reason: neither has a `@verb` or a `@require_permission`
(`grep -rn "@verb(" office365/security/threatintelligence | wc -l` answers `0`), so a marker there
would be written and read by nothing — no page, no `-h`, no denial to attach it to. A stamp is only
worth its claim where something asks.

**Whose seat it is, is declared too.** A marker can say `seat=USER`, which makes the guard read
what the *caller* was assigned instead of what the tenant bought, because those are two facts from
two reads (`subscribedSkus` and `/me/licenseDetails`). Exactly one marker flipped:
`PrivilegedAccessScheduleRequest`, a PIM activation, where the licensed identity is the one
activating. The rest stay `TENANT`, including Intune - the seat Intune requires belongs to the
*device's* user, which is a third question (`subject=`) needing a lookup per device per call, and
the service's own 403 answers it better. See `0005-licence-seat.md`.

One thing used to be missing on purpose, and now is not: **nothing checked that a plan *name*
exists**. `@requires_license("AAD_PREMIUM_P")` and a tenant holding `AAD_PREMIUM_P2` answered the
same way - *not held* - so under `enforce` the typo refused a call the tenant paid for. §5 is that
fix: a committed name set from Microsoft's published list, and a census of the families that sell a
capability. The three split judgements above are `SILENT` entries there, so the next type to arrive
in one of them is a decision instead of a drift.

## 8. Where the code is

| What | Where |
| --- | --- |
| `requires_license`, `licenses_of`, `LICENSE_STAMP` | `office365/permissions/declaration.py` |
| `TENANT` / `USER` / `SEATS`, `Licence`, `licence_of`, `seat_suffix` | `office365/permissions/declaration.py` |
| the seat check and its second reader | `office365/licensing/guard.py` — `held_by_user`, `_check_seat` |
| the fold and the union | `office365/capabilities.py` — `_declarations_of`, `Capabilities.licenses` |
| the licence sentence | `office365/capabilities.py` — `hints_of`, `Requirement.to_hint()` |
| the page line and the `-h` epilog | `office365/cli.py` — `_page`, `command`, `_hints` |
