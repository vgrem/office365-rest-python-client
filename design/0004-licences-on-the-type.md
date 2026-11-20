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
a single method because there was nowhere else to write it.

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
$ o365 search entity query -h
...
This API declares: application Mail.Read, ...; delegated Mail.Read, ...; one of the licences
SPE_E5. (Permissions depend on the entity types being queried)
```

The rule is one sentence per fact: `hints_of` adds its own licence line only when the
declaration's line does not already name exactly those plans. A caller who needs the answer as
data asks `capabilities_of`, which has had `licenses` all along.

Both are read off the model, so no page can claim a licence the type does not declare, and a
type that names none prints no line — `o365 sharepoint web` is unchanged.

## 5. The vocabulary, and the one place it is not yet honest

A licence is named by **service plan**, the vocabulary a tenant's `subscribedSkus` already
carries, and the one `Capabilities.licenses` documents. A SKU part number is packaging: the same
capability arrives inside several SKUs and one SKU turns on dozens of plans, so a requirement
written in plans can be checked against any tenant.

`declaration.py` used to call the field "SKU part numbers"; that docstring is now the paragraph
above, because the ambiguity had already produced one wrong declaration:

```
office365/search/entity.py:49:        licenses=["SPE_E5"],
```

E5 is a SKU. The plan inside it that grants Microsoft Search is not named anywhere in this tree,
so that one declaration keeps the part number. It is a debt with a name, not a silent exception:
`grep -rn "licenses=\[" office365 --include=*.py` is how it stays visible, and it is the only
line it prints.

The other half of the same decision: `graph_client.require_license()` matches either spelling by
substring. It is the legacy reader; `Capabilities.licenses` and the CLI do not use it.

## 6. What was stamped, and why those four

| Type | Plan | Why it is not a permission |
| --- | --- | --- |
| `ConditionalAccessPolicy` | `AAD_PREMIUM` | P1 is what makes the feature exist; no grant creates it on a P1-less tenant |
| `RiskyUser` | `AAD_PREMIUM_P2` | identity protection is P2 |
| `UnifiedRoleScheduleBase` | `AAD_PREMIUM_P2` | a *schedule* is PIM, and PIM is P2 |
| `ManagedDevice` | `INTUNE_A` | managing a device is Intune, so the seat must carry it |

Four, not forty: the point of this note is the mechanism, and a stamp is a claim about licensing
that a person has to be able to defend. These four are the whole claim, so adding a fifth is a
deliberation about licensing, not a copy-paste of a neighbour.

Conditional Access is `AAD_PREMIUM`, not `_P2`: a P1-only tenant can create a policy, and a
marker that refused it would be wrong about the product. P2 buys risk and PIM, which is why the
other two say so.

## 7. Not done

* **No guard.** Nothing refuses a call on a tenant without the licence — `Capabilities` reports,
  the CLI prints, and the request is sent. Enforcing it is a session-level decision (off/warn/
  enforce) and needs the tenant's SKUs, which is a request of its own; it is not a marker.
* **No 403 → licence hint.** A refusal is still reported as a permission problem; the runtime has
  no licence awareness today.
* **Four families, not the families that matter.** Access packages, eDiscovery, records
  management, threat intelligence and Intune reports are the obvious next ones, and each needs
  someone to say which plan it is — the closed set is the place where that answer is written down.

## 8. Where the code is

| What | Where |
| --- | --- |
| `requires_license`, `licenses_of`, `LICENSE_STAMP` | `office365/permissions/declaration.py` |
| the fold and the union | `office365/capabilities.py` — `_declarations_of`, `Capabilities.licenses` |
| the licence sentence | `office365/capabilities.py` — `hints_of`, `Requirement.to_hint()` |
| the page line and the `-h` epilog | `office365/cli.py` — `_page`, `command`, `_hints` |
