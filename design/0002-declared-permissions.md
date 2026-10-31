# 0002 - Declared permissions: one vocabulary, then a matrix

Status: proposed. Applies to `tests/capabilities.py`, `tests/preflight.py`,
`office365/directory/permissions/`.

## Context

The fact "this call runs only if the tenant granted something" is declared in two
places today, in two types, with two different spellings of the same concepts:

| Where | Type | Declares | Size (measured on this tree) |
| --- | --- | --- | --- |
| `@require_permission` on a model method | `PermissionRequirement` | `delegated`, `application`, `directory_roles`, `licenses` | 178 methods in 51 modules, 47 distinct names |
| `@requires_delegated` / `@requires_application` on a live test | `Requirement` | `delegated`, `application`, `roles`, `licenses`, `bypass_roles` | 192 declarations in 147 suites, 123 distinct scope names |

The two sets overlap on 36 names. That means 11 names the model declares are named by
no test, and 87 names the tests declare are named by no model. Some of that is
under-declaration on the model side (178 decorated methods out of 15,057 properties and
1,833 navigations), some of it is tests declaring permissions for endpoints the model
never annotated. Nothing in the tree can tell the two apart, because nothing joins them.

Two smaller findings from the same measurement:

- `PermissionRequirement.directory_roles` is declared zero times, and `licenses` once
  (`SPE_E5`). The test side uses `bypass_roles` 21 times, with distinct role names.
- No test covers `PermissionRequirement`, `__required_permissions__` or `to_hint()` at
  all, although the hint is what a developer reads after a 403.

Three consumers already read a variant of this fact: the `AccessDeniedException` hint,
`preflight`'s report and grant plan, and `guard.py`'s probes. A fourth is coming: a
plan that changes a tenant must state what it needs in order to change it.

## Decision

1. **One type.** `Requirement` becomes library code
   (`office365.directory.permissions.requirement`) because three of its consumers are
   outside the test harness. `tests/capabilities.py` re-exports it so nothing that
   imports it today changes.
2. **Producers, never a list.** A matrix is assembled from declarations:
   - a model method, read from `__required_permissions__`, converted by
     `PermissionRequirement.requirements()` into one `Requirement` per flow it can run
     under;
   - a live test, read from `__requires__` (unchanged);
   - a policy catalog, for the facts neither can state - which scopes are alternatives
     of each other across flows, which directory role stands in, whether the grant needs
     admin consent, which license is required.
3. **The join is flow-aware and lives in the harness.** `matrix()` maps a name to the
   methods and tests that declare it. `preflight` renders it, `--grant` prices it,
   `AccessDeniedException` quotes the line for the call it just made.

Non-goals: no desired-state engine in this step, no hand-written matrix file, no new
HTTP traffic.

## Shape

```python
from office365.directory.permissions.requirement import Requirement

requirement = Requirement(
    delegated=("Sites.Read.All", "Sites.ReadWrite.All"),
    bypass_roles=("SharePoint Administrator",),
)
requirement.describe()  # delegated: any of Sites.Read.All, Sites.ReadWrite.All or role: any of ...
```

A group is an *any-of*; groups are combined with *and*; `bypass_roles` satisfies the
whole requirement. That is the same shape a test already declares, so a model
declaration converts without inventing a field:

| `PermissionRequirement` | `Requirement` |
| --- | --- |
| `delegated=[...]` | `Requirement(delegated=(...))` - one requirement per flow |
| `application=[...]` | `Requirement(application=(...))` - one requirement per flow |
| `directory_roles=[...]` | `bypass_roles=(...)` - a role stands in for the scope |
| `licenses=[...]` | `licenses=(...)` - required, so it rides on both flows |

Per-flow rather than one requirement carrying a flow field: a test always runs under
exactly one flow, so its requirement names one group; a method can be called either way,
so it yields two. The flow is the key of the join, not a property of a permission name.

## Invariants

- **A matrix is a view, never an input.** If it disagrees with a declaration, the
  declaration wins and the view is regenerated.
- **Read a declaration; never call the thing that made it.** `__requires__` on the
  wrapper, `__required_permissions__` on the method.
- **Two-way ratchet.** Every declared name appears in the catalog, and every catalog
  entry is declared by something. Both directions fail on this tree, not on a promise.
- **"Not verified" is not "missing".** A refused permission lookup is `unverifiable`.
- **The offline gate stays offline.** Only the probe (`TenantState.of`) reads a tenant.

## Slices

1. `Requirement` moves to the library, the harness re-exports it, model declarations
   gain `requirements()`, and the 178 model declarations get their first test. No
   behaviour change: offline suite green, preflight output byte-identical.
2. `matrix()` joins both producers; the preflight rows gain "via N declared calls", so
   `--all` answers *which endpoints* a scope unlocks, not just which tests.
3. Catalog plus the two-way ratchet.
4. `--grant` prices the plan from the catalog, so `--dry-run` can say what a grant costs
   before anything is granted.
5. Only then a reconciler (`Desired` / `Actual` / `Plan`) reusing `migration`'s ports,
   with U9 as its first consumer. A plan that changes a tenant states its permissions;
   that is why 1-4 come first.

## Consequences and risks

- Moving a type into the library widens the public API. `Requirement` keeps its exact
  semantics: it is the same dataclass, moved.
- `PermissionRequirement` stays the decorator's argument record, because 178 call sites
  and any user code already spell it. It gains a conversion, it does not change shape.
- The catalog must not become the second list this project keeps deleting. A name that
  nothing declares means a missing declaration, not a missing catalog entry.
- Slice 2 has to explain the 87 names no model declares. Two readings are possible -
  under-declared models or over-declared tests - and the answer decides whether slice 5
  can price a plan at all.

## Open questions

- `@require_permission(directory_roles=...)` means what `bypass_roles` means in the
  harness. Keep the public spelling and document the equivalence, or rename it? Proposal:
  keep it, convert internally; a rename touches 178 call sites for no new capability.
- Does the catalog ship with the library (a user's 403 handler wants it) or stay in the
  harness (it is policy, and policy drifts)? Proposal: library, versioned, with the
  ratchet guarding it.
- The hint currently prints both flows verbatim. With the matrix it could print the one
  flow the failing request used. That is a slice 2 change, and it needs a test that the
  hint names the flow the request actually ran under.
