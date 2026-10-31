# 0002 - Declared permissions: one vocabulary, then a matrix

Status: proposed. Applies to `tests/capabilities.py`, `tests/preflight.py`,
`office365/permissions/` (the declaration machinery) and
`office365/directory/permissions/` (Graph's own permissions entities, unchanged).

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
- No test covered `PermissionRequirement`, `__required_permissions__` or `to_hint()`,
  although the hint is what a developer reads after a 403. That gap is closed:
  `tests/unit/test_permission_declarations.py` exercises the projections, the stamp, the
  query tag (sync and async), the docstring block and the hint text.

Three consumers already read a variant of this fact: the `AccessDeniedException` hint,
`preflight`'s report and grant plan, and `guard.py`'s probes. A fourth is coming: a
plan that changes a tenant must state what it needs in order to change it.

## Decision

1. **One type.** `Requirement` becomes library code
   (`office365.permissions.requirement`) because three of its consumers are
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
4. **A name is a name *on an API*.** A declaration and a requirement carry a
   `ResourceName`, because `Sites.ReadWrite.All` is a grant on Microsoft Graph and a
   different grant on SharePoint, and `Mail.Send` is application-only on Graph while it is
   delegated on Exchange Online. Names from two APIs are never merged into one group.

Non-goals: no desired-state engine in this step, no hand-written matrix file, no new
HTTP traffic.

## Shape

```python
from office365.permissions import Requirement, ResourceName

requirement = Requirement(
    delegated=("AllSites.FullControl",),
    resource=ResourceName.SharePoint,
    bypass_roles=("SharePoint Administrator",),
)
requirement.describe()  # delegated on Office 365 SharePoint Online: any of ... or role on ...: ...
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
| `resource=...` | `resource=...` - the API the names belong to, default Microsoft Graph |

Per-flow rather than one requirement carrying a flow field: a test always runs under
exactly one flow, so its requirement names one group; a method can be called either way,
so it yields two. The flow is the key of the join, not a property of a permission name.

## Invariants

- **A matrix is a view, never an input.** If it disagrees with a declaration, the
  declaration wins and the view is regenerated.
- **One API per requirement.** A group of names is only checkable within one resource, so
  a caller that spans two APIs holds two requirements; `Requirement.join` refuses the
  merge instead of producing a group whose members are not comparable.
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
  and any user code already spell it. It gained a conversion (`for_flow`, which
  `requirements()` uses) and lost the `joined()` classmethod, which was the wrong class
  answering a caller's question - that is `Requirement.join` now.
- The catalog must not become the second list this project keeps deleting. A name that
  nothing declares means a missing declaration, not a missing catalog entry.
- Slice 2 has to explain the 87 names no model declares. Two readings are possible -
  under-declared models or over-declared tests - and the answer decides whether slice 5
  can price a plan at all.
- The consumer side landed ahead of the matrix, because it needed no catalog:
  `@requires_call(Message.send)` derives a test's requirement from the method's
  declaration, and `tests/outlook/test_outlook_user.py` is its first user. Five tests now
  name no scope at all, and two disagreements became visible: the model says
  `Mail.Read` / `Mail.ReadWrite` for `getMailTips` where the test said
  `Mail.Read` / `Mail.Read.Shared`, and the model declares `User.Read` alone where the test
  claimed four alternatives. Both resolved toward the model, since a test that names more
  than its endpoint needs is the over-declaration this slice exists to remove.
- That slice also found the hole the matrix will inherit: `Entity.get` and `Entity.update`
  cannot name a permission, because they cannot know the type they act on. A test that only
  reads an entity therefore still restates its scopes - and those restatements are where the
  test-only names live. The counts quoted above have drifted with the ratchet: 184 declared
  methods in 52 modules, and 2,437 public operations still naming nothing (2,238 of them in
  SharePoint), recorded in `tests/unit/test_permission_declarations.py`.
- Reading the declarations was itself duplicated, and that is now a library concern, with its
  own package: `office365.permissions.declaration` (the marker, `declared()`),
  `office365.permissions.requirement` (`Requirement`, `Requirement.join`) and
  `office365.permissions.index` (one walk of the tree, answering `declared()`,
  `undeclared()`, `debt()`). Two findings came with it. The join belonged in the library
  because three callers wanted it - a live test, the ratchet, and any future `--grant` - and
  the declaration table was being thrown away at import time and rebuilt by an `ast` walk in
  the test file. Swapping the walk for an import-time registry of classes changed no number;
  deleting that registry for a memoized `index(package)` changed two things:
  `runtime` no longer imports the permissions package (no `__init_subclass__` hook, so an
  answer cannot depend on what a process imported first), and the ledger dropped the
  `Query`-suffix rule - 16 builders lost, and with them `ImageInfo.__eq__`,
  `BatchQuery.get_queries` and `AuditLogQuery`. A name suffix is a guess; one rule
  (`add_query` / `execute_query` / `execute_batch` in the bytecode) is worth a floor 16
  methods lower, because it is the same rule the map was measured with, so a new undeclared
  builder still raises a count. Bytecode reading also keeps the old `ast` false positive out:
  a property annotated `-> EdiscoveryReviewSetQuery` is not a request builder. And
  `pkgutil.walk_packages` is still avoided - it skips every namespace-package directory in
  this library, which is why `index()` walks files.
- The resource half of a declaration arrived with a checkable payoff rather than as
  foresight, because two readers were already wrong without it. `verify_permissions`
  hardcoded `ResourceName.Graph` for both lookups, so a SharePoint declaration would have
  been judged against Graph's grants; and `guard`'s cached lookups took a `resource`
  argument, used it as an `lru_cache` key, and then queried Microsoft Graph regardless - a
  wrong answer cached under the right name. Both now resolve the resource's own service
  principal. That made the dimension a one-line change per reader instead of a new
  subsystem, and it had to land *before* the SharePoint harvest: 2,238 declarations
  written without it would each be unpriceable and would need a second pass. The default
  stays Microsoft Graph, so all 184 existing declarations mean exactly what they meant -
  preflight output is byte-identical - and the new `tests/unit/test_permission_resources.py`
  pins the probe to the named resource with a client whose two resources grant different
  things, which is the only way to see the bug: a check satisfied *because* it read the
  wrong API looks exactly like a correct one.
- Those two lookups then turned out to be the *smaller* half of the story, because the
  readers they call were wrong too - and it took a token to see it. Reading the JWT the
  tenant actually issues (43 `roles` for Microsoft Graph, 3 for SharePoint) and comparing
  it with what the readers answer is the only cheap oracle available: the Graph side
  reported 20 of the 43 application permissions the token carried, and answered
  "not granted" for `Mail.Send`, `Mail.ReadWrite` and `Domain.ReadWrite.All` - the exact
  names the Outlook half had just been converted to declare, so 25 of 355 live-suite
  requirements were being skipped for a reason that did not exist. Both causes were shaped
  by the same mistake: reading a relationship the tenant builds incrementally as if the
  first page were the whole of it. `$expand=appRoleAssignedTo` truncates (21 of 43),
  reading one `oauth2PermissionGrants` row loses every other consent, and
  `appRoleAssignedTo` refuses every `$filter` worth writing - so the assignment reader had
  to move to the *client's* side of the same relationship (`appRoleAssignments` filtered
  by `resourceId`), which is both supported and the question being asked. The lesson is not
  "use the token": it is that a permission answer needs a second, independent way to check
  it, and the ratchet cannot tell a false "granted" from a true one because both look like
  a passing test. `tests/unit/test_service_principal_permissions.py` pins the truncation
  with a scripted transport that serves two pages.
- What the token cannot do is replace the grant read, and the remaining disagreement shows
  exactly where the line is. After both fixes, 7 of 355 requirements still disagree, all
  delegated, and all for one reason: `Mail.Send` is delegated on *Exchange Online* and
  `TermStore.Read.All` on *SharePoint*, so the scope reaches the Graph token through
  another resource's grant row and appears in no Graph row at all. A single-resource grant
  read is therefore right to answer "not granted on this API", and a caller that asks it
  about a cross-resource name is asking the wrong question - while the token, which is the
  union over resources, cannot be produced for a scope that was never granted and so can
  never price a grant. Two lenses, two questions: the token says whether the wire will
  accept this call, the graph says what the tenant has granted and what a grant would cost.

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
- Where does a per-type permission go? Reading a `User` and reading a `Chat` need different
  scopes, but both go through one `Entity.get`, which declares nothing. Proposal: declare on
  the type (a class-level requirement) and let the base method fall back to it, so a
  `@requires_call(User.get)` derives what `@requires_call(Entity.get)` cannot.

