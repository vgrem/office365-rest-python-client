# The licence report: what a tenant holds, and what that opens

Doc 61 §5 put `-h` / doctor / completion at `L5` and the catalogue at `L6`. The markers landed
first (`0004`), the seat followed (`0005`), and the guard learned to refuse (`L3`). What was still
missing was the cheapest half of all of it: **the library knows which licence each type needs and
nothing ever said so out loud.** `o365 licences` is that sentence, and this is how it is built.

## 1. The question, and the three it is not

A person looking at a paid family has three questions:

| Question | Answered by |
| --- | --- |
| which licences does a command name? | the markers, via the index — this document |
| does *this* tenant hold them? | `subscribedSkus` — this document |
| which product should I buy for the rest? | `o365 doctor` — not built; see §6 |

The one question the library **cannot** answer, and must not pretend to, is *does capability X
require plan Y*. That mapping is prose in Microsoft's per-feature documentation; the licensing CSV
has the product names and the service plan names but no feature column. So a stamp exists only
where somebody could name the plan (`0004` §5), and this report shows only what was stamped. A
silence in the table is a silence in the declaration, not a claim that the capability is free.

## 2. Where the words come from

`office365/index.json` is the generator's answer to "what can I type", and format `2` adds the
licence each noun's type declares:

```json
"intune.androidforworksettings": {
  "type": "office365.intune.devices.android_for_work_settings:AndroidForWorkSettings",
  "verbs": ["delete", "get", "update", "upsert"],
  "walks": {"GraphClient": {"item": ["device_management", "android_for_work_settings"]}},
  "licence": {"plans": ["INTUNE_A"], "seat": "tenant"}
}
```

`_licence_of(found)` asks the item type first and its collection second, and the second question is
the one that matters: `RiskyUser` (a `User`) and `RiskyUserCollection` (an `EntityCollection`) are
siblings, so a family that stamps the feed and not the item would otherwise read as unlicensed —
which it did, until the fallback. One source for the fact, `office365.permissions.declaration
.licence_of`, asked by both the index and the CLI's page.

Rebuilding the index costs one walk of the tree:

```
$ python -m generator graph --index
2038 nouns over 22 products, 349 walkable, 152 licensed -> office365/index.json (1.1 MB)
```

Read back it costs 34 ms — cheaper than the `find_spec` calls it replaces, which is why the report
can afford to open it.

## 3. The join

`office365/licensing/report.py` is a **pure function of (index document, plan names)**. It imports
no model, sends no request and holds no client, so the tests run without a tenant and the module
cannot quietly become a second catalogue.

| Piece | What it says |
| --- | --- |
| `of(document)` | the declared licences, keyed by `(plans, seat)` and counted by area |
| `area_of(ref)` | `office365.intune.devices.managed.device:ManagedDevice` → `intune.devices` |
| `rows(licences, held, mine=None)` | render-ready records, held first |
| `headline(records, tenant="")` | one sentence: *holds 1 of the 2 licences a command names* |

A licence is keyed by its plans **and** its seat, because one plan is a different claim when one
capability needs the tenant to have bought it and another needs it assigned to the caller. Two
rows, not one row that means two things:

```
PLAN            SEAT    NOUNS  AREAS
INTUNE_A        tenant    131     11
AAD_PREMIUM_P2  tenant     16      4
AAD_PREMIUM_P2  user        3      1
AAD_PREMIUM     tenant      2      2
```

`NOUNS` sums to the index's own `licensed` count — 131 + 16 + 3 + 2 = 152 — which is the check
that the join neither invents nor drops a noun.

The areas are not a cell. A first draft printed them as one — `intune.devices (119),
intune.print (3), …` — which shortened four of eleven names and marked the rest with an ellipsis,
and `-o wide` printed the same comma-joined paragraph without a width, which the terminal wrapped
into soup. The record therefore carries `by_area` as a list, `areas` is `len(licence.families)`
derived from it, and `-o wide` prints one line per area under the plan it belongs to:

```
INTUNE_A        tenant  131 nouns
  intune.devices                           119
  intune.print                               3
  …
```

`HELD` is printed only when some row does not say `yes`: under a headline that already says *all
4*, a column whose every value is `yes` is a header over nothing. A piped format keeps it — and
keeps `areas`, the count — because a machine has no headline to read.

## 4. The two reads, and the word for a read that failed

`o365 licences` makes exactly the reads `LicenceGuard` makes, once each:

```python
held = client.licences.get_all().execute_query().value  # /subscribedSkus
mine = client.licences.get_user(client.me).execute_query().value.plans  # /me/licenseDetails
```

`HELD` is one of three words, and the third is the design:

| Word | Meaning |
| --- | --- |
| `yes` | the plan is provisioned (tenant seat) or assigned to the caller (user seat) |
| `no` | the read answered, and the plan is not in it |
| `unknown` | the read was not made, or it failed |

`unknown` is never turned into `no`. A token without `User.Read.All` cannot see its own licence
details, and a report that read "not held" from a 403 would accuse a tenant that paid — the same
rule as `Requirement.unpublished`: an unread vocabulary is unknown, not absent.

## 5. The command

`licences` is answered before a product is looked for, because it is the one word that asks about
the whole library rather than about one noun. It is a level-0 word like `login` and `completion`,
so TAB offers it before any package is imported:

```
$ o365 __complete --prefix "" --describe | tail -3
completion	shell script
licences	what this tenant holds
help	any of these pages
```

Measured on a tenant holding all three plans (`mediadev8.onmicrosoft.com`, delegated token):

```
$ time o365 licences
mediadev8.onmicrosoft.com: holds 4 of the 4 licences a command names

PLAN            SEAT    HELD  NOUNS  FAMILIES
...
real    0m1.86s
```

1.86 s is two live reads; the join and the render are microseconds on top. `-o wide` prints the
areas as lines under each plan, `-o csv` / `-o tsv` write the counted records for a spreadsheet,
and `-o json` sends them plus the tenant and the plan names they were measured against. The three
piped formats put the sentence on **stderr** and leave stdout to the data, so a redirect keeps the
file clean:

```
$ o365 licences -o csv 2>/dev/null | head -2
plan,seat,held,nouns,families
INTUNE_A,tenant,yes,131,"intune.devices (119), intune.print (3), …
```

`url` and `name` are not offered: they answer for a noun's records, and a plan is not something a
client can address.

## 6. What it deliberately is not

- **Not a catalogue.** Plan → product display (`AAD_PREMIUM_P2` is included in 27 products,
  `INTUNE_A` in 66) is a real answer the Microsoft CSV can give, and it has no home here: this
  report's input is a parsed index and two reads, and growing it into a committed capability table
  would recreate exactly the snapshot `f178f34f1` removed. It belongs in `o365 doctor`, where the
  question "what should I buy" is actually asked.
- **Not a doc.** There is no generated `docs/licences.md` listing families and plans, for the same
  reason: the command answers it from the shipped declarations, and a page would go stale the
  first time a stamp moved.
- **Not a guard.** It reads and prints; nothing here refuses a call. Refusal is `L3`, and it lives
  in `office365/licensing/guard.py`.

## 7. Where the code is

| What | Where |
| --- | --- |
| the licence on a noun, format 2 | `generator/tools/index.py` — `_noun`, `_licence_of` |
| the join, the rows, the sentence | `office365/licensing/report.py` |
| the verb, the two reads, `-o` | `office365/cli.py` — `licences`, `_assigned` |
| the tests | `tests/unit/test_cli.py` (the join, the rows, the sentence, the page) |
