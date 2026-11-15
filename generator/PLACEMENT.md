# Placement contract

How the generator decides where a generated type lives: the decision table the
generator follows, the one pass that re-applies it to files already written, and the
invariant `tests/tooling/test_generator_placement_pass.py` pins.

## Target levels

```
office365/                 package root (config `output_path`)
  <level 1>                product (Graph) or service (SharePoint)
    <level 2>              subsystem
      <level 3+>           finer subsystem / metadata namespace
        <type>.py          one type per module
```

- **Level 1 = product**. `microsoft.graph` is a **container namespace**, not a
  product — it unifies OneDrive, Outlook, Teams, Entra, Intune, … The job of
  routing is precisely to **split that container into products** (`directory`,
  `intune`, `communications`, `outlook`, `teams`, `onedrive`, …).
- **Level 1 = service** for SharePoint (`sharepoint`).
- **Level 2 = subsystem** (curated), for services that have them:
  `intune.devices`, `directory.identitygovernance`, `sharepoint.tenant`, …
- **Level 3+** narrows further, often matching the metadata namespace or an
  existing subpackage.
- `office365.runtime` is **infrastructure**, not a product.
- `office365.common` is for **cross-cutting types** — those genuinely used by
  many products (shared value types, vendor-neutral errors, …) and the final
  fallback when no product can be inferred. It must stay small; anything that
  clearly belongs to one product should not land here.

## Decision order (first match wins)

1. **Attached (sticky)** — a file that already defines the type is reused in
   place; an existing type is **never moved**, and its custom members are never
   removed. Metadata additions are appended only.
2. **Exact OData name** — `[type_routing]` entry keyed by the full name.
3. **Namespace** — `[routing]` prefix, e.g.
   `microsoft.graph.security.* → office365.security.*`.
4. **Exact short name** — `[type_routing]` entry keyed by the class name
   (bare `microsoft.graph.*` types only, so it can never shadow a namespace).
5. **Prefix** — `[type_routing]` `Prefix*`, first match in configuration order.
6. **Fallback** — `"*" → office365.common`.

Then **hierarchical descent**: if the routed directory contains a subpackage
whose (underscore-insensitive) name matches the class-name prefix, the file goes
into it with the prefix stripped —
`AccessReviewError → …/accessreview/error.py`, `PrintSettings → …/print/settings.py`.

## Applying the descent to files already written

Descent answers for a **new** type, and rule 1 makes placement sticky, so nothing ever
revisited the files written before their subpackage existed. A tree therefore grows one
flat layer beside its own subpackages: `devices/management_intent.py` next to
`devices/management/intent.py`. `--place` is that revisit:

```bash
uv run python -m generator graph --place office365/intune            # what it would move
uv run python -m generator graph --place office365/intune --apply-place
uv run python -m generator graph --place                             # the whole model
```

It reads the tree, not the metadata, so it answers in a second and takes the same
`PACKAGE` scope `--audit` does. Two rules keep it from arguing with the tree:

- **a move may shorten a stem, never lengthen one.** `device_status.py` is a decision;
  renaming it back to `device_compliance_device_status.py` re-adds the prefix the parent
  package already says. Such files stay where they are.
- **a move descends, never climbs**, so applying the plan to its own output terminates
  and a second run proposes nothing. `--place` on an already-placed tree is a no-op, and
  that is the invariant the test asserts for `office365/intune`.

## Families

Descent reads the **opening word** of a class name, and some families are not named that
way: every `*AuditRecord` belongs in `audit/records`, with the source word as a subfolder
instead of the stem, so `AuditConfigAuditRecord` used to land flat in `audit/` and
`VivaAuditRecord` in `audit/viva_record.py`.

`generator/planning/families.py` is the table that answers first, and it answers for
both readers -- the renderer and `--place`:

| scope | suffix | folder | source subfolder |
| --- | --- | --- | --- |
| `office365.security.audit` | `AuditRecord` | `security/audit/records` | yes |
| `office365.security.alerts` | `Evidence` | `security/alerts/evidence` | |
| `office365.security.alerts` | `EntityMapping` | `security/alerts/entitymappings` | |
| `office365.security.alerts` | `ObjectIdAction` | `security/alerts/actions` | |
| `office365.security.alerts` | `State`, `Status` | `security/alerts/states` | |

- **the folder says the family**, so the stem drops the family word
  (`ai_agent_evidence.py` -> `evidence/ai_agent.py`);
- **a source subfolder claims the leading word** when it exists, and the stem drops it
  (`viva/audit_record.py`); a folder that does not exist is never created, so an unknown
  source keeps its word (`records/fabric_audit_record.py`) and the later move into a real
  folder is allowed to shorten it;
- **a family names a subtree, not a product**: `*Status` under `office365.security.alerts`
  is an alert's, while `SimulationStatus` stays in `attacksimulations/` where its
  navigation reads it.

Two consequences of the pass meeting a family are explicit rather than incidental: a
family that would re-add a word the class name carries keeps the **stem on disk**, since
that stem is the shorter decision (`AuditConfigAuditRecord` stays `config_audit_record.py`
when it moves); and a file already parked in a source subfolder of the family's folder is
not climbed back out of, because the family cannot see why it went there.

`tests/tooling/test_generator_families.py` pins the table: every `*AuditRecord` under
`audit/` and every `*Evidence` under `alerts/` sits in its family folder, every family
names a folder the tree has, and a type that does not exist yet (`FabricAuditRecord`)
lands where the rule says.

A target file that is already taken is reported as **blocked** rather than overwritten:
that is a duplicate to review, not a move to make. Moved modules have their importers
rewritten in the same pass — textually, over `.py` and `.md`, whole tokens only, so a
module that is a prefix of another is not clipped.

## Invariants

- **Importable**: every segment of a planned module is a valid Python identifier
  (namespaces like `…Windows.10…` are sanitized to `…windows._10…`).
- **Contained**: every written file is under `output_path` (never outside).
- **Sticky**: attached types resolve to their existing file and are never moved.
- **No gaps**: every in-scope type resolves to a module — the fallback bucket
  guarantees it (nothing is silently unrouted).
- **Agreement**: the rule that would route a type points at the directory the file is
  in (or an ancestor of it, for a family the descent has not finished splitting).
  `tests/tooling/test_generator_routing_agreement.py` reads the tree and the rules
  together: a type inside `office365.intune` may not route out of it or to a distant
  branch, and no type outside may route into it. This is what keeps a catch-all from
  silently swallowing another product's types — `Device*` used to route Entra's
  `DeviceRegistrationPolicy` into Intune, and `Cloud*` sent the whole cloud PC family
  to `office365.security` while the tree kept it in the Intune virtual endpoint.

## One module, two types

Placement names a file after the **class**, so two CSDL types that differ only by
namespace resolve to one module — `microsoft.graph.Alert` and
`microsoft.graph.security.Alert` both land in `office365/security/alerts/alert.py`.
The v1.0 snapshot has 12 such modules.

The file holds one class, and `entity_type_name` is written once (a later run never
overwrites it), so the class can answer for a member set it does not belong to.
`generator/tools/type_identity.py` decides from the class's own members: when it spells a
name only the type being built declares, and none that only the name it answers
with declares, the literal is corrected (one line, reported on stdout). When it
spells members of both, the class is **merged** — which name it answers with is
then a placement question, and the audit reports it rather than rewriting it.

## Adding routing (2-stage workflow)

1. `python -m generator <service> --suggest-routing` proposes
   `[routing]` / `[type_routing]` entries for unrouted types.
2. Review and paste them into `generator/settings.<service>.yaml`.
3. `python -m generator <service> --force` generates.

The tool proposes; a human commits. **Routing is never written automatically.**

A family rule names the directory the tree already uses, so a new type needs no
`--place` run to land correctly. What it must never do is name a *category*: `Cloud*`
is a word any cloud product may start with, so the rule that owns the cloud PC family
is `CloudPc*`/`CloudPC*`, and `Cloud*` keeps only what no longer-specific rule claims.
The same reading applies to adjectives: `Windows*`, `Android*`, `Ios*` and `Mac*` each
name a configuration *and* an app subtree, so they stay at the Intune root and the
descent picks the family from the type name; `Win32*`, `WindowsMalware*` and
`WindowsInformationProtection*` name one family each and point at it.

## Declared property metadata

Each generated getter carries its wire name — the OData JSON key — in an
`@odata(name="…")` declaration above the `@property`, and a CSDL
`NavigationProperty` adds `navigation=True` (it is reached with `$expand`, never
named in `$select`). `office365.runtime.types.odata_property` collects the
declarations into `ClientObject._odata_meta`, which is what `declared_type()` and
the write path read.

The name is always taken from the metadata, never derived from the attribute:
`iCalUId` and `icalUid` both survive a snake-case round trip and only one of them
is a real column.

The generator renders only members that are *missing*, so a template change does
not reach files that already exist. Those files were back-filled once, by a codemod
that read the name each getter already queried and validated the literal against the
metadata; it converged (a dry run over every package, under both services, planned
nothing) and has been deleted rather than kept beside a tree it no longer changes.

What that leaves for a human is one rule: **if you hand-write a getter, declare it**,
taking the name from the metadata and never from the attribute -- `iCalUId` and
`icalUid` both survive a snake-case round trip and only one of them is a real column.
`tests/unit/test_odata_metadata.py` holds the other direction: a declaration must
name a wire name its getter actually reads, so a copy-pasted `@odata` cannot silently
take a column out of `TypeSchema.columns`.

For preview-only members and preview types the generator can still rewrite existing
files, because those facts come from a metadata diff and not from a template:

```bash
uv run python -m generator graph --diff-metadata generator/metadata/GraphBeta.xml \
    --apply-markers --dry-run    # @odata(beta=...) and @version("beta") gates
```
