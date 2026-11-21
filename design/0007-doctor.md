# Doctor: what this session can do, before it runs anything

Doc 62 asked for a first-run page and named it `doctor`. `o365 licences` (`0006`) answers the
tenant's half — which plans it holds and how many words each opens. This is the other half, and
it is a different question: **for the command I am about to type, which of the names it needs does
this session already have?**

The answer has to exist before the first command, so it cannot be the service's. Everything here
is read from something already committed — the declarations, the index, and the token in the
session store — plus at most three reads of the tenant.

## 1. Two questions, one word

```
o365 doctor                                  the environment
o365 doctor intune managed-device retire      one command
```

Both are level-0 words answered in `main()` before `_dispatch`, beside `licences`:
neither is about a product. Which of the two forms was asked is the only branch in `doctor()`.

## 2. The environment block

| Line | Read from | Requests |
| --- | --- | --- |
| `graph: … (tenant …, mode …, 75 min left)` | the session store | 0 |
| `  grants: 55 scopes` | the kept token's `scp`/`roles` | 0 |
| `mediadev8.onmicrosoft.com: holds 4 of the 4 licences a command names` | `subscribedSkus`, then `/me/licenseDetails` if a plan is asked of the caller | 1–2 |
| `roles: Intune Administrator, …` | `/directoryRoles` + `/me/memberOf` | 2 |
| the `PLAN / SEAT / HELD / NOUNS / FAMILIES` table | the index joined to the subscriptions | 0 |
| the `PRODUCT / NOUNS / LICENSED` table | the index | 0 |

Measured: `time o365 doctor` → **2.0 s** against `mediadev8.onmicrosoft.com`, in **four**
requests — the two the licence report makes and the two the role read makes — essentially all of
it spent waiting; parsing the index costs 0.007 s. The grants line is a **count**, not
the list: the delegated session there carries 55 scopes and the app-only one 42 roles, and seventy
names would push the table off the screen — `o365 whoami` is the word that lists them.

The `PRODUCT` table has no `usable` column, and that is the decision rather than an omission. A
licensed word is still gated by the permission its call declares, so one number per product would
claim an answer only the licence table — plan by plan, seat by seat — can give. `LICENSED` counts
the words that name a plan at all, which is a fact about the model; `HELD` is a fact about the
tenant, and it belongs to the row that names the plan.

## 3. One command

```
o365 intune managed-device retire  (write)

FACT         NAMES                                                    STATE
delegated    DeviceManagementManagedDevices.PrivilegedOperations.All  missing
application  DeviceManagementManagedDevices.PrivilegedOperations.All  unknown
licence      INTUNE_A                                                 have

unknown is not missing: this token does not answer for that name, and the tenant's grant might
needs  a session that holds: DeviceManagementManagedDevices.PrivilegedOperations.All
```

**Five facts, four sources, no call.**

1. The route comes from `route(*words)` — one product package imported, nothing sent. It already
   answers `.entity/.verb/.here/.method`, and a page (no `.verb`) is refused with the words it
   does answer, a typo with the close matches the router computes.
2. One row per flow in `FLOWS`, because a declaration names two alternatives and which one applies
   is the session's answer, not the model's. Marks come from `TokenClaims.proves()`, i.e. from the
   token's own `scp`/`roles`.
3. A `licence` row when the declaration names plans, marked through `answer()` — the same function
   `o365 licences` uses, so the two pages cannot disagree. The plans themselves come from the
   **type**: `capabilities_of(found.here)` folds the family's stamp into every member's
   declaration, which is why a call is asked the same question as the type it lives in.
4. One `role` row per `directory_roles` name, from the same role read the environment block
   makes (`/directoryRoles` and `/me/memberOf`, matched on `roleTemplateId`).
5. `state` is `have`, `missing`, or `unknown`, and `unknown` is the licence report's word for a
   read that did not happen. Two reads can be absent — the token (no session, or one that kept no
   token) and the tenant (a token without `Licence.Read.All`). Neither is evidence of absence, so
   neither prints `missing`, and one sentence says which it is.

Only the licence and role rows send anything, and only when the declaration asks for them: a
command that names a permission and no plan is answered by a stale token, offline.

## 4. What is refused, and with what code

| Asked | Answer | Exit |
| --- | --- | --- |
| a word the router cannot reach | `did you mean …` on stderr | 2 |
| a noun without an action | `names a page, not a command; it answers: …` | 2 |
| an action the model does not describe | `declares no permission: nothing about this session decides it` | 0 |

The third is a report, not a refusal: the tree publishes no marker, so no token could fail it, and
turning a gap in the library into an error of the caller's would be the wrong accusation. It is
also the row a person needs to see — a command that declares nothing is a debt, not a permission.

## 5. What is not here

- **No `setup`.** Doc 62's next step needs a project-owned public client id, which does not exist
  yet; `login` and `--client-id` already cover the same ground for a person who has one.
- **No product→plan advice.** Nothing here says *buy this to get that*: the licensing CSV names
  products and service plans and has no feature column, so the sentence would be invented.
- **No second catalogue.** `licensing/report.py` still takes a parsed index and the plan names
  already read; plan-to-product display stays in this page, where a session is at hand.
- **No lifecycle hook on the runtime.** The page reads the store and calls the client; nothing was
  added to `ClientRuntimeContext` for it.
