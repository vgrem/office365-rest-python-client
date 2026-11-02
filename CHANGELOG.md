# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

Two stories. The model types now *declare* the metadata they read, so `$select`,
`$expand`, comparison, provenance and throttling limits are derived from one
declaration instead of hand-written at each call site. And the migration layer
became a set of portable trees — mail, calendar, contacts, lists, navigation —
built on those types, so a source and a target spell an item the same way.

### Breaking

Three of these reach shipped API — `Web.site_id`, the `SP.User` profile getters and
the `NavNode`/`WebNavigation` records; the rest re-shape what this development line
introduced.

- The Teams export archive is the model's own JSON: `team.json` is
  `team.to_json()` with `members`, `installedApps` and `channels` attached, and
  `messages.ndjson` lines are `message.to_json()` plus `channel_id`. `TeamRecord`,
  `ChannelRecord`, `MemberRecord`, `TabRecord`, `AppRecord` and the extractor
  behind them are removed; `TeamsExportOptions` moved to
  `migration.teams.adapters`.
- Every mailbox sidecar is the model's own JSON with Graph's keys —
  `Message.to_json()`, `Event.to_json()`, `Contact.to_json()` — plus the three
  provenance keys a model cannot know. A tree written by a pre-release build is
  refused by name (`refuse_legacy_sidecar`) instead of importing as empty fields.
- SharePoint getters declare the OData names they read (4,013 declarations,
  back-filled from the CSDL). `Web.select_all()` goes 39 → 118 columns and
  2 → 50 navigations, `List` 21 → 98, `File` 11 → 37, `Field` 3 → 41; a
  projection built from the old lists asked for navigation properties, which
  `$select` drops silently. Request bodies are unchanged — a declaration says what
  a *response* may carry, never what a request must.
- Graph getters declare the OData names they read: 6,911 declarations in 1,057
  modules, back-filled from `Graph.xml` and its preview snapshot. `select_all()` is
  derived from the declarations, so projections grow: `User` 21 → 81 columns,
  `Group` 13 → 53, `DriveItem` 10 → 32, `Team` 9 → 17, `Channel` 5 → 13,
  `AccessPackage` 6 → 11. 175 members that were declared as columns are now declared
  as the navigations they are, so `$select` no longer asks for them — Graph drops
  those silently, the same failure the SharePoint half had. Request bodies are
  unchanged.
- The back-fill that wrote those declarations has been retired, not kept beside the
  tree it no longer changes: a dry run over every package under both services planned
  nothing, and what guards them now is a test that reads each declaration against the
  getter it sits above — one `created_by` in the SharePoint half carried its
  neighbour's name, so `CreatedBy` was unmapped and `expand_all()` never asked for it.
- An enum-typed Graph column returns the member, not the wire string: 386 type
  imports in 241 modules moved from the getter's own body (and the dead
  `if TYPE_CHECKING:` entry beside it) to the module block — 403 columns, because
  one import serves every getter that names it — so `declared_type` can see what
  the annotation says. `BrowserSharedCookie.source_environment` is
  a `BrowserSharedCookieSourceEnvironment` rather than `'2'`; compare by
  `.name`, which is what the service accepts back. A value no member names is
  kept as the service sent it instead of being coerced to `None`; a value that differs
  from a member only in case is that member, because one service spells one value set
  two ways (`GET /teams/{id}` says `public`, the group it was listed from says `Public`).
- A complex-typed Graph column declares its type as well: 592 `ClientValue` imports
  in 328 modules moved the same way, and 745 more columns answer the type they name
  (1,760 value-typed columns in total). Writes behave as before — a getter that builds
  its default instance already hydrated the value — but a column with no declared type
  was *skipped* by the record importer as unknown, so
  `coerce_records(BrowserSharedCookie, [{"history": …}])` dropped that column with
  `Skipping unknown column 'history'` and keeps it now.
- The names only a dead `if TYPE_CHECKING:` block binds are reachable too: 25 imports in
  21 modules moved out of the block (66 of the sites are `Optional` in
  `sharepoint.listitems.listitem`), and 145 of the 149 columns that still raised
  `NameError` now answer a type — `ListItem.created` is `datetime`, not `None`. The four
  left are the cyclic value types (`ChatInfo`, `ConditionalAccessGrantControls`). A
  `timedelta` column now *declares* `timedelta` while still holding `'PT30M'`: the
  declaration is this change's job, the converter is the next one.
- `SP.User` loses the 58 profile getters that were a second copy of
  `SP.Directory.User` (`about_me`, `skills`, `id_`, ...), plus
  `User.get_user_profile_properties` and `Web.site_id`. The service drops those
  names from `$select` silently; the profile fields live on
  `sharepoint.directory.users.user.User` (63 declared) or behind
  `PeopleManager.get_user_profile_properties`.
- `NavNode` and `WebNavigation` are removed: a captured navigation is the model's
  own tree, read through `Web.navigation.get_tree(recursive=True)`.
- `MigrationItem` no longer carries `author_id`/`editor_id` — they are
  `item.author.user_id` / `item.editor.user_id`, and the old keywords raise
  `TypeError`. `ItemReport` keeps both columns.
- `PagePayload` is gone (a page item is a `SitePage`), `PAGE_LIBRARY_TEMPLATE`,
  `SITE_PAGE_CONTENT_TYPE_PREFIX` and `is_modern_page` left
  `migration.sharepoint.pages` in favour of `is_page_library(list)`, and
  `offline_context()` moved up to `office365.migration.offline`.
- `IcsProfile` is `IcsDialect`, and each family's record is one class with methods
  rather than a record type plus free functions: `CalendarEventRecord` and its
  `event_*` helpers are `EventRecord`, the `contact_*` helpers are
  `ContactRecord`, and `STANDALONE_EVENT_TYPES`/`event_kind` are gone.
- The permission-declaration machinery moved out of the Graph namespace into its own
  package: `office365.permissions` exports `require_permission`, `declared`,
  `PermissionRequirement`, `Requirement`, `Requirement.join`, `ResourceName` and `index`. The
  old `office365.directory.permissions.require_permission` / `.requirement` / `.registry`
  modules are gone, as is `.resource_name` (it is `office365.permissions.ResourceName` now); a
  model method announces what its request needs, and `declared(method, flow=...)` reads it,
  raising instead of answering an empty requirement when the method names nothing under that
  flow. `office365.directory.permissions` keeps Graph's permission entities (`Identity`,
  `IdentitySet`, ...), which are model types, not vocabulary.
- A declaration and a requirement now name the **API resource** its permissions belong to
  (`@require_permission(resource=ResourceName.SharePoint, delegated=["AllSites.FullControl"])`).
  A permission name is only a grant on the API that defines it - `Sites.ReadWrite.All` is
  granted separately on Microsoft Graph and on SharePoint, and `Mail.Send` is an application
  permission on Graph but a delegated one on Exchange Online - so names from two resources are
  never merged into one requirement (`Requirement.join` refuses). The default is
  `ResourceName.Graph`, which is what every existing declaration means, so rendered
  requirements are unchanged. Two readers that had assumed Graph are fixed: `guard`'s cached
  lookups used `resource` only as a cache key while querying Microsoft Graph, and
  `verify_permissions` hardcoded it.
- `office365.sharepoint.workflow.task` is gone, with the second `SPWorkflowTask` it declared.
  Its 25 operations were a strict subset of
  `office365.sharepoint.workflow.sp_workflow_task.SPWorkflowTask`'s 32, and nothing in the
  library, the tests or the examples imported either class — two classes wearing one metadata
  name, which also made the declaration index count the same endpoints twice. The survivor is
  the one that says what it is (`SP.Workflow.SPWorkflowTask`) rather than inheriting the
  generic `SP.ListItem`; import from it.

### Added

**Model metadata**

- A field can declare what the service treats as the same value:
  `@odata(name="birthday", compare=Compare(format="date"))`
  (`office365.runtime.types.odata_property.Compare`: `casefold`, `fallback`,
  `default`, `unordered`, `format`, `ignore`, `key`). `entity.to_json(COMPARABLE)`
  (`office365.runtime.odata.comparable`) spells a model in that comparable form,
  so two copies that differ only by what the service rewrites — an address-only
  email named after itself, a birthday's time of day, a label set's order, a
  fractional second — compare equal and a real difference does not. It is one more
  `JsonProfile`; `V4JsonFormat` output is unchanged.
- `hydrate(payload, profile=None)` is the one in-place read verb on
  `ClientObject`, `ClientValue` and `ClientResult`, answers `self` so it chains,
  and `profile=None` reads what `to_json()` writes with no profile.
  `JsonProfile.scoped(Model, only=..., without=...)` narrows any profile to some
  properties of one model, and `ClientValue.odata_name` mirrors
  `ClientObject.odata_name` so a scope narrows a value too.
- `JsonProfile` keeps only what it uses: four accessors that re-exported a dialect
  field (`metadata_type`, `collection`, `collection_next`, `etag`) are gone.
- One serialization contract (`office365.runtime.serialization`:
  `JsonSerializable.to_json(profile=None)`, `PropertyReceiver.set_property(name,
  value, persist_changes)`), structural, nothing inherits from it.
- Getters declare their OData name in place, so nothing spells a name twice:
  `declared_type(Event, "iCalUId")` now answers `str`, `@odata(navigation=True)`
  marks an `$expand`-only member, and `Event.select_all()` returns the 41 names
  `$select` accepts, `expand_all()` the 7 `$expand`-only ones,
  `odata_name("ical_uid")` the wire spelling. An enum-typed property reads back as
  the generated enum member.
- Every `$select` column of a served package resolves a declared type, including
  the twelve value-object getters that carried no annotation, or one naming a type
  imported only under `TYPE_CHECKING` — either way hydration read a bare dict where
  the model promises a value object.
- `@odata(..., expandable=False)` marks a navigation `$expand` will not follow
  alone: `Event.expand_all()` no longer names `extensions`, which the service
  refuses without a `$filter`.
- `@odata(..., system=True)` records provenance: the metadata declares no such
  name, the service spells it on the item payload. `ListItem.author_id`,
  `editor_id`, `created`, `modified`, `SitePage`'s three item columns and
  `Tenant.displayName`/`id`/`serviceInfo` say so — the flag is derived by the
  codemod (absent from the CSDL ⇒ `system`) and answered by `TypeSchema.system`.
- `ClientObject._unselectable` states the columns a type's own service refuses to
  project (`Web` answers 400 for `DescriptionTranslations`; a `ListItem` refuses
  `Client_Title`, `DisplayName`, `IconOverlay`). The declaration survives for
  hydration and comparison, and `select_all()` leaves the name out.
- `@key("tenantId")` declares which property spells a *type's* identity, above the
  class next to `@version`: what re-anchors an entity's path when the value is set,
  and what a read forces into `$select`. No declaration means the family default
  (`id` for Graph, `Id` for SharePoint), so a class that states nothing behaves
  exactly as it did; a composite key raises `CompositeKeyNotSupported` rather than
  half-addressing. Nine v1.0 Graph types were addressed by `id` that no request can
  satisfy (`WorkflowVersion` is keyed by `versionNumber`,
  `CrossTenantAccessPolicyConfigurationPartner` by `tenantId`,
  `AuthenticationConditionApplication` by `appId`, …); the generator now derives
  the declaration from the CSDL `<Key>` — `--plan-keys` reports, `--apply-keys`
  writes, and a mode the metadata cannot be trusted for (`keys_authoritative=False`,
  SharePoint states 613 keys, 284 of which name a member no class has) refuses to write at all.

**Outlook mail**

- `MessageCollection.add_from_mime(data)` creates a draft from RFC 822 bytes —
  an `.eml` file as it sits on disk — posting them base64-encoded as
  `text/plain`, the one Graph create whose body *is* the message.

**Migration**

- `IdentityMap` (`office365.migration`) maps source principals onto target
  principals for authorship and ACLs, so a run can cross tenants: entries from a
  CSV (`source,target[,system_id]`), e-mail domain rewrites, and a policy for
  unmapped principals (`skip` / `fail` / `fallback_owner`). Unmapped principals
  are reported, never silent. `MigrationSettings.user_mapping_file` feeds it and
  `automatic_user_mapping=False` turns it off — both were previously listed as
  unhonored.
- Mail as a portable tree: `MailFolderSource` + `MailExportTarget` write one
  `.eml` plus one JSON sidecar per message and a `manifest.jsonl` index, with
  destinations derived from the message so a resumed run skips what is on disk;
  `EmlTreeSource` + `MailboxTarget` import it back through `add_from_mime`,
  recreating the folder chain, skipping messages by `internetMessageId`, and
  replaying read state, categories and importance. Each family has its options
  class — `MailExportOptions`, `MailImportOptions` and a matching pair per family
  — and mail is verified by `mime_digest` — the semantic
  headers plus a hash per decoded part — because Exchange re-serializes every
  message it stores, so the bytes are never the same.
- `MigrationItem.metadata` carries adapter-defined envelope attributes (a mail
  message's subject, recipients and categories) into the manifest, so a portable
  export writes its own index; the runner never interprets it.
- Calendars: `CalendarSource` + `IcsExportTarget` write one `.ics` (CRLF, RFC 5545
  folding, `TZID`, `RRULE`, `VALARM`, `X-ALT-DESC`) plus a sidecar per event;
  `IcsTreeSource` + `CalendarTarget` import it, replaying Graph's own
  `recurrence` object from the sidecar (an `.ics` alone is refused). Attendees are
  opt-in, because creating an event with attendees makes Exchange send a real
  invitation.
- Contacts: `ContactSource` + `VcfExportTarget` write one `.vcf` (vCard 3.0, folded
  at 75 octets) plus a sidecar per contact; `VcfTreeSource` + `ContactTarget`
  import it, restoring every office field, address, phone, IM address, child, note
  and category.
- `MigrationJob.plan()` states the fidelity forecast before it enumerates
  (`plan.fidelity`, `MigrationJob.fidelity()`, `export_reports`), and
  `describe_fidelity` reports a product's own dimensions instead of always
  printing SharePoint's fourteen: an adapter may declare
  `fidelity_dimensions`.
- `SharePointPackageTarget` and the library/list record targets accept a captured
  structure (`sp_list=` / `structure=`) and replay it before the first write, so a
  bundle can be imported into a library that has none of its shape. Verification
  reads each verified record once per run, and a source/target that disagree about
  files versus records are refused when the task is resolved instead of at the
  first write.
- The server-side package target grants SharePoint **groups** as well as users:
  `PermissionEntry.principal_type="group"` plus `owner`/`owner_groups`, because a
  `<Group>` without an `Owner` fails the whole ingestion job at schema validation.
- `FileVersion.sort_key` compares version labels as numbers (`"1.9"` before
  `"1.10"`), and `BasePermissions.value` / `from_value(mask)` own the 64-bit
  permission mask in both directions — no caller derives the shift.
- A page's fields are spelled by the library
  (`office365.sharepoint.publishing.pages.fields`: `PAGE_FIELDS`, `BODY_FIELDS`,
  every name derived from `SitePage`), and `SPBuiltInContentTypeId.SitePage` is
  the content type base a modern page derives from. `SitePage` declares the three
  item columns it answers (`file_leaf_ref`, `wiki`, `moderation_status`) and the
  two writable content properties, with the page predicates (`is_modern`,
  `is_classic`, `body`, `body_field`) and the write (`apply_page_payload`) on the
  type.

**Long-running operations**

- An operation is watchable, not just waitable: `stream()` / `astream()` on every
  poller yield each snapshot, terminal one last, and raise nothing for a failed
  outcome. `wait()` is the same loop with the failure policy applied.
- `OperationStatus` carries the operation's timeline (`created_date_time`,
  `last_action_date_time` timezone-aware with UTC fallback, `retry_after`), and a
  `partiallySucceeded` operation is terminal-but-neither-outcome instead of an
  unknown status that polled until timeout.
- `RespondAsyncRequest.execute()` returns an operation either way: pollable when
  the service answered `202`, already terminal when it finished in the submitting
  round-trip (`LongRunningOperationResult.completed(...)`, `is_completed`).
- One engine behind every wait (`office365.runtime.operation.Operation`): deadline,
  `Retry-After` pacing, jitter, progress hook, cooperative cancel, and
  `transient_statuses=` as data. `OperationPoller` and `PollableOperation` are
  specialisations of it, so `PollableOperation` gains `stream()` and `cancel()`.
- `MigrationServerJob.job_wait()` returns the wait instead of running it, so polls
  can be streamed, cancelled or monitored concurrently; a sync `status_fn` given to
  an async wait is bridged with `asyncio.to_thread`.

**Service limits**

- Graph's throttling quotas are data: one `quotas` module per product
  (`outlook`, `teams`, `onedrive`, `onedrive.workbooks`, `reports`, `security`,
  `directory`, `communications`) plus `GLOBAL_QUOTAS` (130,000 requests / 10 s per
  app), each registering itself at import. `office365.limits.catalog(product=...)`
  answers from a fresh interpreter, `catalog_products()` lists the keys, and
  importing `office365.limits` imports all of them. A row states where its number
  comes from, and a concurrency ceiling appears where the service states one. The
  rows are reference only: the library reacts to the server signals it already
  parses and does not simulate a token bucket.
- A model **references** a row instead of re-spelling it (`CALL_RECORD_QUOTAS`,
  `EXCEL_QUOTAS`), and a quota is declared where the request is made, not on the
  type whose name it mentions — including on a method, where a declaration may sit
  on the operation that makes the call (`CallRecord` carries the table, and
  `sessions`/`participants_v2` its per-resource row; `PSTN_RECORD_QUOTAS` rides
  the direct-routing call listing).
- `@limit` **composes**: a second decorator on one target adds its rows instead of
  replacing the first, and stacked declarations share one `Limits:` section.
  `declared_limits()` answers each row once, reads `@limit` off the MRO, and
  `limits_of(cls)` now answers class-level rows too, de-duplicated by
  declaration.
- 97 of the 122 published rows are now reachable from some `_schema`, up from a
  handful. The 25 that are not are named rather than forgotten: Teams' 12 default
  rows (a default names no resource), one security surface this library does not
  spell, two SharePoint rows that describe an object it does not address, and the
  10 OneDrive/files rows whose bindings are still to come. The Service limits page
  is generated from both registries, so a published number cannot drift from its
  declaration.

**Permissions**

- **The migration layer names what it needs, and the ledger has no package left to exempt.**
  The 54 public request-issuing operations under `office365.migration` declare their grant: the
  37 SharePoint ones as a `@site_access` rung (`capture_*`/`read*` are `READ`,
  `apply_*`/`provision_*`/`write` are `WRITE`, `copy_site_pages`, `apply_navigation`,
  `apply_site_security` and `apply_permissions` are `MANAGE`), the Outlook ones as Graph names,
  and the two thin wrappers (`MailboxTarget.checksum`, `MigrationServerJob.progress_async`)
  borrow theirs with `@derived_from`. `migration` left `UNTRACKED`, so
  `index(office365).debt()` is `{}` for every package rather than `{}` for the packages that
  were asked. Two shapes have no single name to give and say so in `notes` instead of inventing
  one: `MigrationJob.assess` submits whatever assessor it was handed, and
  `TeamsArchiveSource.read` fans out across endpoints whose own declarations name them.
- **The request detector counts the async twins.** `_SUBMIT` now includes
  `execute_query_async` and `execute_batch_async`, which made ten tracked operations visible
  for the first time (three of them methods on private download-plan classes). Most were already
  covered by the rung of the synchronous twin they mirror — `File.download_session_async`,
  `File.get_content_stream_async`, `FileCollection.create_upload_session_async`,
  `Entity.execute_batch_async` and `ClientContext.execute_batch_async` — and two needed a
  declaration of their own. Widening belongs in this batch rather than after it: declaring
  `MigrationServerJob.progress` while the identically-bodied `progress_async` stayed uncounted
  would have put the ratchet's hole exactly where an awaitable caller stands.
- **A wrapper borrows the declaration of the method it drives.** `@derived_from(callee)` stamps a
  method with the *same* `PermissionRequirement` the callee carries — read once at import — so a
  one-line pass-through has no second copy of the rung to drift from, and `help()` names the
  method whose request the columns describe. The three server-side migration calls are the
  motivation: `MigrationServerJob.submit`, `submit_encrypted` and `progress` declare nothing
  themselves, they call `Site.create_migration_ingestion_job`,
  `create_migration_job_encrypted` and `get_migration_job_progress`. Borrowing *silence* fails at
  decoration instead of yielding an empty requirement every check would pass. The exactness is
  not free: it ties `server_job`'s import to the SharePoint model tree, so `MigrationServerJob`
  and `MigrationJobWait` joined `office365.migration`'s lazy re-exports — that import stays 56
  modules, none of them SharePoint.
- **A permission check can read the token itself.** `office365.permissions.TokenClaims`
  parses a JWT's payload and answers one requirement: the audience says which API the token
  was issued for, `scp` names the delegated permissions, `roles` the application ones. The
  signature is never checked - the token this process obtained came over TLS, and one handed
  in was accepted or refused by whoever took it - so it is a *parse*, and a token it cannot
  read (opaque, not a JWT, another audience's, the other flow) answers `None` rather than an
  empty set, because a silence must not be read as "not granted".
- Both authentication contexts expose `access_token`, acquiring it once if they hold none
  yet, so a caller can ask what a token proves before sending a request and the answer does
  not depend on whether a request already ran. That makes a SharePoint-only suite decidable
  with the one credential it has: measured, the Graph app-only token carries 43 `roles` and
  the SharePoint app-only token `Sites.FullControl.All`, `Sites.ReadWrite.All` and
  `TermStore.Read.All`.
- The convenience methods on `GraphClient` — `has_`/`grant_`/`get_`/`revoke_`, delegated and
  application — take `resource`, defaulting to Microsoft Graph, and `--grant` passes the one
  its plan names. `Sites.FullControl.All` is a Graph permission and a SharePoint one, so a
  helper that assumed Graph could report a SharePoint gap and then grant it to the wrong API.
- **SharePoint declarations start, and the resource switch is proved end to end.** 20 methods
  of `Web` and `SecurableObject` now name what they need on `ResourceName.SharePoint` — a read
  ladder (`Sites.Read.All`, `Sites.ReadWrite.All`, `Sites.Manage.All`, `Sites.FullControl.All`)
  and a management one — and `tests/sharepoint/test_web.py` derives its preconditions from
  them: 24 tests pass under an app-only certificate, 1 skips for a reason that has nothing to
  do with permissions. The package's debt moves 2,238 → 2,228. A method that only builds a
  path (`Web.get_list` hands back a `List` the caller sends) is still the place to declare:
  it is the operation with a name, and the general read verb underneath (`Entity.get`)
  cannot know its type.
- A live test's skip decision reads that token first and the tenant's grants only where the
  token cannot speak. A grant read is scoped to one API, so it cannot see a delegated name
  granted on another: `Mail.Send` lives on Exchange Online and `TermStore.Read.All` on
  SharePoint, and the grant read reported 7 of 355 requirements as missing that the token
  says are granted. Measured after the switch: 0 false skips, 0 false passes.
- **A permission name is checkable with no tenant.** `office365.permissions.catalog(resource)`
  answers what an API publishes — `Catalog.publishes(name, kind)`,
  `requires_admin_consent(name, kind)`, and the names themselves — generated by
  `scripts/gen_permission_catalog.py` from that API's own service principal (`appRoles` for
  application permissions, `oauth2PermissionScopes` for delegated ones) and committed under
  `office365/permissions/snapshots/`. Only the facts that decide whether a grant is possible
  are kept (published, enabled, user-consentable), because a description is edited freely and
  would be churn in every regeneration. The tree's 89 distinct (API, flow, name) pairs are
  checked against the 777 + 867 names Microsoft Graph publishes and the 20 + 29 SharePoint
  does, so a name its API does not publish fails offline. A snapshot is refreshed by re-running
  the script, which is also the only way to notice a name Microsoft retired: the tenant refuses
  it and the harness reads the refusal as "not granted", so live nothing distinguishes a typo,
  a retired name and a real gap. This is what makes the remaining harvest reviewable — a wrong
  name used to be indistinguishable from a grant that was never given.
- **SharePoint's ladder is one word per method.** Its eight names are four rungs —
  `AllSites.Read` → `.Write` → `.Manage` → `.FullControl`, with `Sites.Read.All` →
  `Sites.ReadWrite.All` → `.Manage.All` → `.FullControl.All` beside them for app-only — where
  each rung already does what the ones below it do. So `office365.sharepoint.permissions`
  exports `SiteLevel` and a decorator that fills in both flows and the resource:
  `@site_access(SiteLevel.WRITE)`. The rung is the *weakest* grant that works, because
  over-claiming would skip a live test on a tenant that could have run it. `List` declares 88
  methods this way and `Web` 97 more, and the 20 hand-written declarations were rewritten as
  the same one-liner — six lines each, still naming the same names by hand. Debt 2,228 →
  2,043, and 30 live tests across 16 SharePoint suites now derive their precondition from the
  declaration of the method they call.
- **The everyday objects carry the rung too.** `File` declares 51 methods, `ListItem` 35 and
  `ListCollection` 5 — the part of the tree where the rung has to be judged one method at a
  time rather than read off a name: `File.get_content` reads, `File.recycle` writes,
  `File.change_content_storage_schema` manages a library's schema, and the three sharing-link
  calls on an item (`share_link`, `unshare_link`, `delete_link_by_kind`) manage permissions.
  `ListItem.ensure_type_name` declares `READ` even though it sits on the write path, because
  all it queues is a read of the target list. Debt 2,043 → 1,952, and 15 live tests across 6
  suites derive their precondition from the declaration. The one operation left unmarked is
  the private `ListItem._set_taxonomy_field_value`: a helper that is not an entry point names
  nothing, so it stays in the debt.
- **`Site` declares 70 methods, and 31 of them needed a second answer.** 39 stay inside the
  site collection — `exists`, `open_web`, `get_web_templates` and the four `get_progress_for_*`
  readers take `READ`, the version-policy and block-download calls `MANAGE` or `WRITE`,
  `run_upgrade_site_session` and `create_preview_site` `FULL_CONTROL`. The other 31 act on the
  tenant: the migration API, copy jobs, bring-your-own-key, hub site registration,
  `update_inactive_site_properties`. No rung grants those on its own — they also want a
  SharePoint administrator — so `site_access` grew one optional argument and they read
  `@site_access(SiteLevel.FULL_CONTROL, role="SharePoint Administrator")`, the role declared
  as the *alternative* it is (`Sites.FullControl.All` still grants provisioning, and an
  administrator needs no grant at all). The 11 tenant-scope *reads* among them name `READ` and
  the role, following the same rule as everywhere else: the weakest grant that works. Debt
  1,952 → 1,882, and 12 live tests across 6 suites derive their precondition from the
  declaration. This corrected a harness assumption too: a bypass role the client cannot look
  up — a SharePoint-only suite has no Graph surface to read directory roles from — used to make
  the whole requirement unverifiable, so four tests skipped for a reason that had nothing to do
  with the tenant. An alternative that cannot be checked is not a permission that is missing,
  and the names still decide; a role or SKU the requirement *holds* is part of the answer, so
  failing to read that is still unverifiable rather than unmet.
- **A blocker now says which calls asked for it.** The written preflight report gives a
  requirement a `via` column — the 40 SharePoint tests blocked on `Sites.Read.All` name
  `Web.get_catalog`, `Site.exists`, `File.copyto` — because a grant twelve tests need and a
  grant *one endpoint* brings are different decisions: the first is an administrator's
  problem, the second is a call we could stop making. `@requires_call` stamps the calls as
  `module:qualname`, the identity `Operation` is keyed by, so a row names an operation the
  declaration index can be asked about; `--markdown` prints the column and `--json` lists the
  same names as `calls`. The provenance is kept *beside* the requirement rather than on it:
  two tests that need the same grant are one row however many methods each of them exercised,
  and a requirement stated by hand with `@requires_delegated` names no call and shows none.
- **A checkout can answer "run live" for itself.** An IDE's test runner is handed a path,
  not a command line, so a suite selected in VS Code's test tree or PyCharm's was skipped
  with `live tests are opt-in: pass --live to run them` and nowhere to pass it.
  `OFFICE365_LIVE=1` in `.env` is now that switch: `.env` already reaches the environment,
  so every runner in the checkout signs in — the test tree, a debugger, a bare `pytest` —
  and `--offline` still wins for the run that must not. CI has no `.env`, so it stays
  offline. The skip reason, the session header and `python -m tests.doctor` all name the
  switch instead of assuming a terminal; the flag itself is unchanged, and a runner that
  can hold arguments should still use it.
- **Nothing writes `.env`, nothing generates it, and the wizard is gone.** The program that
  discovers credentials and grants what the live suites declare used to merge its findings
  back into the repo-root `.env`, leaving a `.env.bak` and `chmod`-ing both. That writer had
  in fact stopped working — its merge helper was removed without its call site, so
  `python -m tests.setup` raised `NameError` before doing anything. Everything it did that is
  still worth doing lives where the thing it acts on lives: the certificate and the secret
  come from the example scripts that create them
  (`examples/entraid/applications/rotate_cert.py` now prints
  `OFFICE365_CERT_THUMBPRINT`, `rotate_secret.py` already printed the secret once), and the
  grant loop moved to `python -m tests.preflight --grant` — the module that already computes
  the plan, and now applies it, asks before changing anything, and re-reads the tenant
  afterwards. `tests/setup.py` (428 lines) is deleted; `.env.example` is the skeleton, the
  file holds an app secret and the admin account, and a program that can rewrite a secret
  file can also truncate one. Flags that existed only to fill a printed block went with it
  (`--sites`, `--site`, `--username`, `--username-alt`, `--shared-mailbox`, `--with-password`,
  `--no-password`, `--pick-users`, `--new-app`, `--dry-run`).
- **Tenant administration declares what it needs.** The
  three service-wide objects — `Tenant` (284 operations), `SiteMoveService` (86) and
  `Office365Tenant` (43) — now name a rung and, where the permission alone does not decide,
  the SharePoint Administrator role: 413 declarations, 183 of them reads and 230 writes, and
  nothing left undeclared in those modules. This half of the SharePoint harvest needs no
  per-method judgement, because every operation is tenant-scope: a read takes
  `Sites.Read.All`, a write `Sites.FullControl.All`, and both take the role. 18 live tests
  derive their preconditions from those markers, and the package's debt moves 1,882 → 1,469.
- **A directory role is named once instead of spelled by hand.** `office365.permissions` exports
  `DirectoryRole`, a `str` enum carrying Entra's own `displayName` for the roles this library
  and its tests mention — `SharePointAdministrator`, `GlobalAdministrator`,
  `PrivilegedRoleAdministrator`, `ComplianceAdministrator`, `ComplianceDataAdministrator`,
  `RecordsManagement`. The declaration side compares that string against the tenant's
  directory, and a misspelling there does not fail: it names a role nobody holds, so the
  requirement is simply never met, and on a client that cannot read roles at all the answer
  is *unprovable*, which passes. Both directions hid the typo. `role=` still takes a plain
  string for a name the enum does not list, since Entra's catalogue is far larger than the
  six. The 444 SharePoint declarations that also need the role now use it.
- **The six page kinds and the workflow task declare.** The publishing package is one
  operation set worn six ways: `SitePage` (33 operations), `SitePage3D`, `RepostPage`,
  `TopicSitePage` (23 each), `FeedVideoPage` (27) and `CampaignPublication` (46) all carry the
  page actions, and all of them live inside the site collection, so they take a rung and no
  directory role. 175 declarations, 25 reads and 150 writes, judged one name at a time: nine
  operations that start with `Get` are POST service operations whose answer is data
  (`AmplifyHistory`, `LoadMailDraft`, `SPSiteValidator`, the publishing statuses) and declare
  `READ`, while the co-authoring calls (`StartCoAuth`, `SavePageCoAuth`, `ExtendSessionCoAuth`)
  look like bookkeeping and declare `WRITE`, because each holds or commits a lock.
  `SPWorkflowTask` adds 31 (6 reads, 25 writes): the three `ValidateUpdate*` calls persist the
  item with the validation riding along, and the progress readers only report. The two portal
  managers are tenant-scope like the administration surface, so `GroupSiteManager` (36) and
  `SPSiteManager` (19) declare 34 reads and 21 writes with the Administrator role as an
  alternative — they are reached from `ClientContext` and create site collections. Debt
  1,469 → 1,183, and 1,474 → 1,188 undeclared operations including the 25 the duplicate module
  had been contributing.
- **Teams declares its whole surface.** All 21 operations that put a Teams request on the wire
  now name what Microsoft Graph documents for the endpoint — 15 writes and 6 reads across
  `Team`/`TeamCollection`, `Channel`/`ChannelCollection`, `ChatCollection`, conversation
  members, chat hosted content, schedule change requests and the two activity-feed senders —
  and `teams` leaves the ratchet map with nothing undeclared, as `outlook` did. The name sets
  are the any-of sets Graph publishes (`Team.Create`, `Directory.ReadWrite.All`,
  `Group.ReadWrite.All` for a team; `TeamSettings.ReadWrite.All` and its two alternatives for
  archive), which are the same sets the suites already wrote by hand in `@requires_delegated`;
  the harvest moved that knowledge onto the methods. Those test markers stay as they are: each
  also carries `bypass_roles` for the tenant's administrator roles, and a role is a live-run
  escape hatch rather than a grant, so it belongs in the test and not in the declaration.
  Three endpoints — the three `getAllMessages` exports — are application-only, so they declare
  `application=` and no delegated column at all.
- **Communications declares every operation, and the calls subtree is application-only.**
  18 methods name what Microsoft Graph documents for the endpoint: the five presence writers
  (`Presence.ReadWrite` for the signed-in user's own presence, `Presence.ReadWrite.All` for
  any), `getPresencesByUserId` (`Presence.Read.All`), `createOrGet`
  (`OnlineMeetings.ReadWrite`), `getAllRecordings` (`OnlineMeetingRecording.Read.All`),
  `getVirtualAppointmentJoinWebUrl` (`VirtualAppointment.ReadWrite`) and
  `getDirectRoutingCalls` (`CallRecords.Read.All`). The eight call-control operations —
  `cancelMediaProcessing`, `reject`, `unmute`, `updateRecordingStatus`, `invite`,
  `logTeleconferenceDeviceQuality` and the two hold-music calls — have no delegated column at
  all: the committed snapshot shows Graph publishes `Calls.AccessMedia.All`,
  `Calls.InitiateGroupCall.All` and `CallRecords.Read.All` as application roles, and the
  delegated half of that subtree is empty, so a delegated client can neither be granted the
  name nor honestly be told it lacks it. Checking the names against the snapshot before the
  edit is what caught this: a plausible `Calls.*` scope would have failed the offline
  published-name check, which is the whole reason that check exists. Both flows are named per
  method rather than through a helper, because unlike SharePoint's four rungs these are
  unrelated grants — one operation wants media access, another a meeting, another a
  recording. `communications` leaves the ratchet map with nothing undeclared, as `outlook`
  and `teams` did, and nine live tests derive their precondition from the declaration
  instead of restating the scope by hand. Debt 1,540 → 1,522.
- **Directory declares every operation, and seven of them answer a signed-in user.**
  61 methods across 25 modules: the app-registration writers (`ApplicationCollection.ensure`
  and the four `ServicePrincipal` credential calls — `addKey`, `addPassword`,
  `addTokenSigningCertificate`, `removePassword`), the authentication-method writers
  (`resetPassword`, `enableSmsSignIn`, `disableSmsSignIn`), the two registration reports, the
  lifecycle-policy membership verbs, `uploadClientCertificate`, `availableProviderTypes` on
  both provider collections, invitations, the `directoryObjects` functions (`getByIds`,
  `getAvailableExtensionProperties`, `validateProperties`, `add`, `remove`, the four member
  queries, `restore`), the authentication-strength policy update and its `usage` report, the
  risk decisions (`confirmCompromised`, `dismiss`), the backup-protection `activate`/
  `deactivate`/`run`/`deleteAndUnprotect` verbs, synchronization `pause`/`start`/`functions`,
  cross-tenant lookup, and fourteen `User` actions. Seven of those name no application role,
  because no app-only token can satisfy them: `filterByCurrentUser` on app-consent and
  user-consent requests filters by *the signed-in user*, and `ThreatAssessment.ReadWrite.All`
  (the four assessment creators) and `UserActivity.ReadWrite.CreatedByApp` (`/me/activities/
  recent`) are published as delegated scopes with no application role behind them. Where
  several grants genuinely work the declaration says so instead of picking one: `$ref`
  membership takes any of `Directory.ReadWrite.All`, `Group.ReadWrite.All`,
  `GroupMember.ReadWrite.All`, `RoleManagement.ReadWrite.Directory` or
  `AdministrativeUnit.ReadWrite.All` — the collection being added to decides which — `restore`
  takes the write grant of whichever object type is being restored, the member queries also
  accept `GroupMember.Read.All`, the calendar views `Calendars.Read` or `Calendars.ReadWrite`,
  and `findTenantInformationBy*` accepts `Organization.Read.All` beside
  `CrossTenantInformation.ReadBasic.All`, which is the gate the suite already passed.
  `directory` leaves the ratchet map, the fourth package to do so; debt 1,522 → 1,461, and
  eleven live tests now derive their precondition from the declaration rather than restating
  the scope by hand.
- **The drive declares every operation, and a file's grants come as a rung.**
  62 methods across 26 modules under `office365.onedrive`: `DriveItem` (nine, including
  `preview`, `getContent`, `getFiles`/`getFolders`, the resumable upload and
  `extractSensitivityLabels`), `Drive` (`recent`, `search`, `sharedWithMe`, `createBundle`), the
  two site objects, the web-part position, the sharing calls (`PermissionCollection.add`,
  `Permission.grant`), the version restore, the container activation, and 36 that belong to the
  workbook. The item operations do not pick a name each. Graph publishes the file permissions
  twice — `Files.*` and `Sites.*` — because a drive can be someone's OneDrive or a document
  library and the same item is reachable through either, so the declaration lists the whole rung
  (six names for a read, three for a write) and any one of them satisfies it: the shape the tree
  already used for `DriveItem.get` and `ensure_folder`. The workbook is the opposite case: all 36
  declare `Files.ReadWrite` (or `Files.ReadWrite.All`), reads included, because a workbook
  session is opened by a write grant and the reads happen inside it — the four workbook
  declarations already in the tree say the same, and this batch agrees with them rather than
  inventing a read rung the endpoint never checks. Two methods reach across the tenant and say
  so: `getAllSites` takes the read rung and `removeSites` `Sites.FullControl.All`. Two more name
  something other than a grant: `FileStorageContainer.activate` declares
  `FileStorageContainer.Selected` with the SharePoint Embedded Administrator role in its note,
  and `DriveItemCopyResult._resolveItem` — a private helper that does put a request on the wire,
  to read the item the copy produced — declares the write rung it inherits from the copy. That
  last one is the rule working rather than an exception to it: a private helper that builds no
  request names nothing. `onedrive` leaves the ratchet map, the fifth package to do so, and 26
  live tests derive their precondition from the declaration instead of restating the scope by
  hand. Debt 1,461 → 1,399.
- **Tenant configuration and compliance name their grants, and the policy store speaks for
  Purview.** 126 methods across eight modules: `SPPolicyStoreProxy` (23 — 8 reads, 15 writes),
  `SPHSite` (18), `SiteScriptUtility` (17) and the two copies of the data-governance insight
  client (16 each) are tenant-scope, so they declare `FULL_CONTROL` for the writes and `READ`
  for the readers with the SharePoint Administrator role beside them — the same reading the
  administration surface got. Two owners do not reach that far: `SiteManagerService` (18 — 7
  reads, 11 writes) answers for one site collection, so its eleven writers that activate
  features and provision lists declare `MANAGE` rather than `FULL_CONTROL`, and the two
  `TemplateAPI` (9 each) live in a content type hub, which is a site again. The policy store is
  the exception: retention labels, holds and adaptive scopes are administered in Microsoft
  Purview although the request goes to the site's own `_api/complianceStore`, so it names
  `DirectoryRole.ComplianceAdministrator` — the first use of that member — as the role that
  satisfies it. Two of the eight modules are duplicates nothing imports
  (`contentcenter/template_api.py`, `tenant/administration/datagovernance/insight_client.py`).
  They are declared anyway: the ratchet counts the code that is there, and a duplicate that
  can still be called still asks the tenant for a grant. Debt 1,399 → 1,273, and six live tests
  (the site design and site script suites) derive their precondition from the declaration
  instead of running against whatever the tenant happens to allow.
- **Social and site content name their grants, and the brand center is two owners in
  one class.** 118 methods across six modules: `PeopleManager` (24), `MicrofeedManager`
  (18), `SocialFeedManager` (17), `SitePageService` (17), `BrandCenter` (26) and the
  e-sign `DigitalLegacy` (16). Most of them are a site rung — the feed posters and likes
  declare `WRITE`, the feed readers and profile lookups `READ`, and the publishing
  service's eight page and image writers stop at `MANAGE` because enabling the categories
  or creating the asset folder changes one site's pages. `BrandCenter` is not one owner:
  thirteen of its methods talk about tenant themes and org assets — the `org_assets`
  lookups, the `*_tenant_theme` reads and writes, the `ensure_*_feature` provisioning —
  and declare the tenant rung with the SharePoint Administrator role, while the six that
  add, update, delete or apply a *site* theme and remove a brand font stay on the site.
  `PeopleManager` splits the same way: `hard_delete_user_profile`, the two OneDrive quota
  writers and the quota-max read are tenant administration hiding in a profile class.
  `DigitalLegacy` is a user's own beneficiary settings, so `WRITE`/`READ` and no role.
  Debt 1,273 → 1,155, and nine live tests (user profile, publishing, client-side
  components) derive their precondition from the declaration.
- **Tenant plumbing names its grants, and the flow runners are tenant work.** 115 methods
  across seven modules: `Automations` (23), `SPMachineLearningHub` (16), `SearchService`
  (16), `TeamChannelManager` (16), `CatalogManagementCustomPropertiesCollection` (16),
  `Folder` (14) and the Viva `EmployeeEngagement` (14). Three of them reach past a site
  collection and declare the tenant rung with the SharePoint Administrator role:
  `Automations` creates and deletes Power Automate flows and their connections, which
  belong to the tenant and not to the web that happens to host the proxy;
  `TeamChannelManager` promotes, demotes and archives the site behind a Teams channel; and
  the catalog custom-property collection is tenant administration by construction. The
  machine-learning hub is a Syntex content center — a site again, so `MANAGE` for its six
  writers. `SearchService` declares one write (`record_page_click`, which records an
  analytics hit) and fifteen reads, since a query, a suggestion and an export all read.
  `Folder` is ten writes and four reads, and the Viva surface is eleven reads and the two
  like/unlike writes plus dashboard personalization. Debt 1,155 → 1,040, and thirteen live
  tests (folder, search, Viva, teams) derive their precondition from the declaration.
- **The last nine product packages leave the ratchet map.** 38 methods across 24 modules:
  Intune's nine remote actions (`wipe`, `retire`, `remote_lock`, `reboot_now`,
  `locate_device`, `shut_down`, `sync_device`, `set_primary_user`, `remove_primary_user`),
  device registration, effective permissions, the two audit enumerations and
  `incidentReport`; the BackupRestore verbs `browse`, `offboard`, `cancel_offboard`,
  `search` and the two service-app switches, plus the common `RestoreSessionBase.activate`;
  four report readers and report submission; retention-label creation; the hunting query;
  the two subscription verbs; four Todo writes; three Planner creates; and two Bookings
  calls. Two of them corrected a plausible guess. `client.devices` registers a *directory*
  device (`microsoft.graph.Device`), so it declares `Directory.AccessAsUser.All` delegated
  and `Device.ReadWrite.All` app-only, not an Intune grant; and `getEffectivePermissions`
  reads the RBAC configuration, so it declares `DeviceManagementRBAC.Read.All` rather than
  the trio that governs the audit endpoints. `office365.subscriptions` is the one place the
  two columns disagree about existence: Graph publishes delegated subscription scopes and no
  application scope, because an app-only token watches a resource it was already granted, so
  those two methods declare the delegated column and leave the application one empty with a
  note saying why. Debt 1,040 → 824, and twelve live tests (todo, planner, intune, booking,
  defender, Purview) derive their precondition from the declaration instead of restating the
  scope by hand. `sharepoint` is the only package still carrying debt, so the ratchet map is
  one line.
- **The eleven largest SharePoint owners declare their rungs.** 121 methods: the followed
  content of the current user (13), the publishing video item (12), the workflow deployment
  service (12), the dynamic-content update service (11), the tenant app catalog accessor
  (11), the theme manager (11), the personal cache (11), approvals (10), the navigation REST
  service (10), search settings (10) and `SP.Utilities.Utility` (10). The judgment is
  per method, not per class: `FollowedContent` reads status and lists with `READ` but
  `follow_item`, `stop_following`, `set_item_pin_state` and `refresh_followed_item` write;
  `VideoItem` returns embed codes, playback URLs and view counts with `READ` while the two
  counters, the owner, the people and the custom thumbnail are writes; the navigation service
  reads eight values and `MANAGE`s the two that save them, because navigation is a
  site-collection setting; and `Approvals` splits creating, approving, rejecting and
  cancelling a request (`WRITE`) from enabling the service, its notifications and its
  properties (`MANAGE`). Three owners reach past their own site collection and name the
  SharePoint Administrator role beside the rung: the tenant app catalog accessor, the theme
  manager (tenant themes are tenant state, and a read of them is still tenant state) and
  search settings, whose one writer is `setxssearchpolicy`. Debt 824 → 703, and six live
  utility tests derive their precondition from the declaration.
- **The eight owners at nine and eight operations each.** 67 methods: the app instance in a
  site (9), the SharePoint directory provider (9), the tenant administration group (9), the
  directory helper (8), the crawl-version provider for tenant search administration (8), the
  two social following managers (8 each) and `MoveCopyUtil` (8). The split is between the
  tenant's directory and the site's own state: creating an app instance, recycling it,
  restoring it and upgrading it are `MANAGE` on the site, while `get_app_database_connection_string`
  only reads; the directory provider and the tenant administration group reach past the site
  collection and name the SharePoint Administrator role, and the provider's two
  `get_or_create_unified_group*` calls are directory writes at `FULL_CONTROL`; `SPHelper` reads
  membership, owners and site availability seven times and `MANAGE`s the one call that removes
  external members; the two social following managers are one operation set worn twice, as the
  SharePoint and the REST spelling of the same user's followers; and every `MoveCopyUtil` entry
  is a write, because copying a file is still writing one. Debt 703 → 636.
- **The fifteen owners at seven and six operations each.** 94 methods: the business-data
  catalog of a site (7), the machine-learning model (7), the second navigation service (7),
  the shared-with-me view (7), the directory session (6), the file version collection (6),
  the related-item manager (6), the smart wiki library utility (6), the corporate catalog app
  metadata (6), the microfeed store (6), the site page collection (6), the recycle bin item
  collection (6), the tenant DDI adapter (6) and the two Copilot agent-insights clients (6
  each). The interesting splits are the ones where "delete" is not one thing: emptying the
  recycle bin, emptying its second stage and moving items there are `MANAGE`, while
  `restore_all` is a `WRITE`; a site page's `add`, `create_app_page` and `update_full_page_app`
  stop at `MANAGE`, as every other publishing writer does; and the wiki library's
  `ensure_smart_wiki_library_feature` is the one `FULL_CONTROL`, because activating a feature
  is a site-collection setting, beside two `MANAGE` batch conversions. The corporate catalog's
  `deploy`, `remove`, `retract` and `upgrade` touch the tenant app catalog and name the
  SharePoint Administrator role; `install` and `uninstall` act on a web and stop at `MANAGE`.
  The tenant DDI adapter and both Copilot agent-insights clients are
  `Microsoft.Online.SharePoint.TenantAdministration`, so all three carry the role, and their
  report *creators* are `WRITE`. Debt 636 → 542, and the recycle-bin suite's last test derives
  its precondition from the declaration.
- **The sixteen owners at five operations each.** 80 methods, and this tier is where the
  "one class, one answer" shortcut stops working entirely. Business data splits three ways:
  `TypeDescriptor` is five reads of BDC metadata, `EntityFieldValueDictionary` reads two and
  writes the two that build an entity instance, and `AppBdcCatalog` (previous batch) sets
  connections with `MANAGE`. The list home is three helpers of the signed-in user - favorites,
  pinned items and recommendations - so each reads one and writes four. `Field` is five
  `MANAGE`s, because a field's index and its presence on a form are list schema, not content.
  `ObjectSharingInformation` is five reads: it asks what the current user *may* do and who a
  thing is shared with, it does not share. `WebPartDefinition` is five `MANAGE`s on a page.
  `WorkflowSubscriptionService` is five `WRITE`s - unregistering interest is still writing.
  Three carry the SharePoint Administrator role: `SPOWebAppServicePrincipal` (five
  `FULL_CONTROL`s of SPFx secrets and third-party app ids), the site properties collection
  (five tenant reads, so the lock state and the archive check do not invent a write), and
  `UserProfile`, whose three personal-site creators provision a site collection and stop
  nowhere short of `FULL_CONTROL`, beside two `WRITE`s of the user's own settings. Debt
  542 → 462, and two more live tests derive their precondition - the sharing report and the
  personal-site provision.
- **The twenty-two owners at four operations each.** 89 methods, and the tier's shape is
  "one name per verb": `EntityInstance` reads two XML forms and writes the two that build an
  instance; `FileCollection` writes the three that add a file and reads the published one;
  `FavoriteListsSubstrate` and `SocialRestThread` read one and write three. Three answers are
  worth recording. `FieldCollection`, `ViewFieldCollection` and `SiteVersionPolicyManager` are
  entirely `MANAGE`, because a field, a view's columns and a document's version policy are all
  list schema rather than content. `DocumentId` stops at `MANAGE` for its resets and reaches
  `FULL_CONTROL` only to set the site prefix - a site-collection setting, not a library one.
  `CommunicationSite` creates a site collection, so `create` and `enable` are
  `FULL_CONTROL` beside the SharePoint Administrator role while the two status reads stay
  `READ`. Four owners are tenant scope and name the role outright: the migration-center parse
  result, the catalog management collection (four reads - exporting a catalogue's display
  names does not write it), the restricted-content-discovery collection and the data-access
  governability client. `ProfileLoader` reads three profiles and provisions personal sites in
  bulk at `FULL_CONTROL`. `ActivityLogger` is four writes of telemetry, and
  `ClientPeoplePickerWebServiceInterface` - both spellings - is five reads of the directory
  from inside a site. Debt 462 → 373, and three more live tests derive their precondition:
  the communication site that the suite then operates on, three view-field edits, and the
  profile loader.
- **The thirty-nine owners at three operations each.** 117 methods, and the tier is where
  the site's own furniture is separated from the tenant's. The site's: a content type
  collection is three `MANAGE`s, the navigation nodes and the view's schema are `MANAGE`, the
  two principal collections and the role definitions are `MANAGE`, and the web part manager
  reads two exports but `MANAGE`s an import. A time zone `set_id` is `MANAGE` - a regional
  setting of the web. Deleting or updating any SharePoint `Entity` is `WRITE`, declared once on
  the base class instead of on the four hundred subclasses. The tenant's, with the SharePoint
  Administrator role: the app-service principal public surface, the content security policy
  configuration, `TenantSettings` (two catalogue switches at `FULL_CONTROL`, one report config
  read), the search administration providers (recycle-bin discoverability, content-processing
  status, ranking judgments, semantic enqueue), and the log export, which is
  `Microsoft.Online.*` and therefore reads with the role. Three answers that could have gone
  either way: `DocumentSharingManager.update_document_sharing_info` stops at `MANAGE` because
  the documentation asks for `ManagePermissions`, while `RichSharing`'s three email shares are
  `WRITE`; `Campaign` and the portal launch waves are publishing objects, so they `MANAGE`;
  and the portal navigation cache wrapper is three `MANAGE`s that mirror the structural
  navigation one. Debt 373 → 256, and three more live tests derive their precondition: adding
  a user to a site group, reading a role definition, and the sharing report capabilities.
- **The sixty-three owners at two operations each.** 126 methods, and the pair is usually one
  word apart: `like`/`unlike` on a comment, `restore`/`move_to_second_stage` in the recycle
  bin, `get`/`set` on a site logo, a news-distribution setting, a spotlight configuration or a
  workflow's external variable. The tenant keeps naming the role where it reaches past a site
  collection - hub sites, tenant admin settings, the site-collection management service, site
  properties, tenant CDN, tenant insights reports, and the two copies of the data-governance
  SAR client that the same class is published under twice. `GeoExperience` is two
  `FULL_CONTROL`s of a multi-geo tenant mode switch. The migration-center storage and the
  performance data read with the role and the storage does not read at all. Four answers worth
  keeping: a query's `SortCollection` is two reads because a sort shapes a read;
  `DocumentId`-style site furniture is not the only `MANAGE` family - custom actions, role
  assignments, content-type field links, multilingual settings and hosted-app web part data
  are all `MANAGE` too, while a user's own first-run experience, their followed items and
  their AI tokens are `WRITE`; `RecycleBinItem.restore` is a `WRITE` and
  `move_to_second_stage` a `MANAGE`, the split the collection already had; and
  `SharingUtility`, `ThemeInfo`, `WorkflowServicesManager` and `PeopleCollection` are pure
  reads. Debt 256 → 130, and two more live tests derive their precondition: the recycle-bin
  restore and the webhook subscription.
- **The last owner on the list, and the end of the debt.** 130 methods in 128 modules - one
  each, which is where a harvest stops being a judgment and starts being a spelling: a site
  group owner, a feature activation, an event receiver, a custom action, a view, a subweb, a
  document set, an alert, an event receiver registration, a list template read, a term store
  search. The tenant's remaining surface names the role: `HubSite.delete`, the third-party
  AAD permission grants, the web-app service principal's permission requests, the malware
  stream, the ODB license enforcement sweep, the tenant app flag, the SharePoint home
  acronyms and the copilot insights reports. Four families answer the same way every time -
  every `Microsoft.Online.SharePoint.MultiGeo` job stop is a `WRITE` with the role and the
  two site read-only-state setters are `FULL_CONTROL` with it, the four consumer quota
  migrations are `WRITE` with it, the download-operation plans are three `READ`s that share
  one method name, and the two pairs of duplicate modules (`DfDeprecationJob`,
  `MoveSiteROState`) are declared rather than deleted. The ledger is empty: `PENDING` is
  `{}`, `index(office365).debt()` returns nothing, and every one of the 2,224 public
  request-issuing operations under `office365/sharepoint` names the grant it needs. Twenty-three
  commits from the first `SiteLevel` to the last dot-notation read, and the two offline
  permission tests now guard the whole surface instead of a shrinking remainder.



### Changed

- **A declaration carries no fact nobody reads.** `ODataPropertyMeta` and
  `@odata(...)` accepted `filterable`, `sortable`, `searchable`, `nullable` and
  `description`; of the 4,883 declarations in the tree, not one set any of them, and
  no code read them. Four of the five have a different owner anyway — whether a name
  is legal in `$filter`/`$orderby`/`$search` is a *product's* answer
  (`QueryCapabilities`, a deny-list per product, because Graph states it in prose and
  neither snapshot states it as a capability: the `searchable` matches in `Graph.xml`
  are properties named `isSearchable`), a description is the getter's docstring,
  written from the same OpenAPI summary, and `nullable` would describe a request rule
  nothing enforces. Passing one now raises instead of being accepted and ignored.
- **An export is a projection of the type, not of the response.** Every writer that
  goes through `records.iter_records` (CSV, TSV, JSON, NDJSON, Excel, Parquet, ORC,
  Feather, SQL, DuckDB, dataframe) used to derive its columns from the page it had
  just read, sorted — so an item carrying an extra field reordered every header, a
  declared column the service left out of a page vanished instead of arriving empty,
  and the column set differed between two pages of the same query. The columns are now
  the type's declared ones, in declaration order, spoken in the client's own service
  root: `Message` exports 31 columns to a v1.0 client and 34 to a beta one, and a
  preview-only name the page happened to carry is dropped rather than exported. A name
  the metadata does not describe — a list item's site columns — still follows, sorted,
  so nothing the service sent is lost; `.select(...)` still means exactly what it names.
- **A list item's own columns are declared on the item.** `ListItem` declares
  `AuthorId`, `EditorId`, `Created`, `Modified`, `FileRef` and `FileLeafRef` as
  `system=True`; `file_system_object_type` answers the enum instead of the wire's
  number, and `is_file` / `is_folder` read that column rather than the presence of
  an expanded `File` part.
- **A navigation node answers the flags the service sends.** `is_visible` and
  `is_external` read `IsVisible`/`IsExternal` (they read `isVisible`, so every node
  on every site answered `None` and the migrator's "copied visible" warning could
  never fire). The node declares nine projectable columns and two navigations,
  six of them `readonly` because the service assigns them; `Navigation` declares
  `UseShared` and both bars as navigations. `add()` sends the two fields that are
  the whole create contract. Measured live: a node created or merged with
  `IsVisible: false` reads back `true`, so a hidden node cannot be copied hidden.
- **A securable declares the ACL flag it has always read.**
  `has_unique_role_assignments` is `readonly=True`, so a response reports it and a
  request never carries it; `FirstUniqueAncestorSecurableObject` and
  `RoleAssignments` are navigations, so they leave `select_all()`.
- **`Field` answers what a column holds**, so a reader need not parse its schema:
  `is_taxonomy`, `is_lookup`, `is_person`, `is_multi_valued`, `is_multi_choice`,
  `is_value_object`, over the two named facts `schema_property(schema_xml, name)`
  and `is_taxonomy_column(type_as_string, schema_xml)`. The classification is keyed
  by `TypeAsString`, not by the Python class — a `Type="Note"` replayed from a
  schema is still a term column — and `AllowMultipleValues` stays declared on the
  types the metadata gives it to (`FieldLookup`, and so `FieldUser`) while
  `is_multi_valued` reads the row, because a column created from a
  `Mult="TRUE"` schema keeps the single-value spelling.
- The runtime now owns the spelling facts the migrator had duplicated: `iso_z` /
  `wall_clock_text` own the two date spellings a SharePoint write takes,
  `normalize_guid` asks `uuid.UUID` (so a braced, 32-hex or `urn:uuid:` id keys
  the same and never travels as a request payload), and `checksum(data)` is the
  one byte-identity helper beside `digest()` for meaning.
- The calendar's spelling, document and record are three modules
  (`calendar_profile`, `calendar_codec`, `calendar_models`), so a Graph enum that
  gains a member is a table row and a test fails if a row names a member the enum
  does not declare. One `SidecarRecord` base carries the on-disk contract for all
  three families (`model`, `provenance` — exactly three keys, asserted at class
  definition —, `legacy_keys`, `identity`, `columns`, `options_class`), with
  `ServiceSource`/`SidecarTreeSource`/`SidecarTreeTarget` owning the two seams;
  `sidecar_required` is the one legitimate family difference (`False` for mail,
  since RFC 822 bytes are complete on their own).
- The bundled transports bound the read and write phases as well as connect
  (`(10 s connect, 300 s read)`; httpx adds write and pool). A server that stops
  responding mid-response now fails as a transient transport error, which
  `with_auto_retry` retries, instead of blocking the caller forever. The read bound
  is a per-byte gap, so a transfer that keeps moving is unaffected.
- `MigrationJob.plan()` fails fast on a fidelity flag the adapter pair cannot
  honour, one phase before the first write.
- `LongRunningOperationResult.monitor_url` is `str | None`, so "no monitor URL" is
  a state rather than an empty string; the ingestion-job monitor counts its
  deadline on the clock instead of adding `interval` per iteration;
  `PollableOperation.wait(sleep=None)` can be woken by `cancel()`.

### Fixed

**Model**

- **A Teams schedule entity sent the service's timestamps back.** `ChangeTrackedEntity` declares
  `id` and `lastModifiedBy` readonly, but `createdDateTime` and `lastModifiedDateTime` were still
  writable, while the CSDL marks both `Org.OData.Core.V1.Computed` — so a shift, a time-off or an
  open-shift update could carry the two stamps it had just been told.
- **Three upload sessions sent a range the service refuses.** Graph requires every
  upload-session range to be a positive multiple of 320 KiB; `AttachmentCollection.resumable_upload`
  defaulted to `chunk_size=1000000` and `Message.upload_attachment` to `1000000 * 3`, and
  `Task.upload_attachment` to 4 MiB — none is a multiple, and neither of the first two validated the
  value at all. All three now default to 10 MiB (32 x 320 KiB) and raise `ValueError` before the
  session is created, from one module (`office365.runtime.transfer`) that also owns the 3 MiB
  threshold at which a mail or To Do attachment stops being posted in a single request.
- **Activating a directory role was refused for the type name in its own payload.**
  `DirectoryRole` extends `DirectoryObject` and inherited the base `entity_type_name`, so the
  `POST directoryRoles` every activation builds announced itself as
  `#microsoft.graph.DirectoryObject` and the server answered "Invalid payload '@odata.type':
  'microsoft.graph.directoryObject' is not a subtype of 'microsoft.graph.directoryRole'" — a
  message about the payload, naming nothing the caller passed. It now says
  `#microsoft.graph.DirectoryRole`. Nothing had ever activated a role, which is why the wrong
  type could sit there unnoticed.
- **`DirectoryRoleCollection.assign` failed with no subject.** Activating a role the tenant has
  never held means posting the id of its template, and a name with no template left the lookup
  `None` and asserted from inside a response listener — an `AssertionError` naming neither the
  role nor the caller. It raises `ValueError("this directory publishes no role template named
  ...")` instead. Found the hard way: `preflight --grant` planned `Records Management`, a Purview
  portal role with no Entra template, and died on it.
- **`Team.messaging_settings` read the guest settings.** The getter spelled
  `guestSettings` in its body, so a team that had messaging settings answered as if it
  had none, and writing it back put the guest settings on the wire under a name they
  were not read from.
- **`SignIn.location` read the status.** The sign-in's city, state and country came
  back as an empty `SignInLocation` for every audit record, because the getter spelled
  `status` — the name a neighbouring getter already owned.
- **`FileStorageContainer.entity_type_name` named no namespace.** It answered
  `graph.fileStorageContainer`, the only entity type name in the tree that does not
  start with `microsoft.graph.`, so a payload it serialised carried a type name the
  service has never heard of.
- **A team listed from the group collection answered a string for `visibility`.**
  `TeamCollection.get_all()` lists `GET /groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')`
  and copies each group into a `Team`, and the two endpoints spell one value set two
  ways: `GET /teams/{id}` sends `public`, `GET /groups/{id}` sends `Public`. `parse_enum`
  matched by value and by exact member name only, so `'Public'` named no
  `TeamVisibilityType` member and — an unfamiliar value being kept as sent — the getter
  answered the string, where `team.visibility.value` raised `AttributeError`. A name that
  differs from a member only in case is now that member, once the exact value and exact
  name lookups have failed; the Teams examples read `.name`, the spelling the service
  accepts back, instead of `.value`.
- **An enum column kept the wire string.** The generator writes a getter's type as a
  function-local import plus an `if TYPE_CHECKING:` entry, and both are invisible to
  `typing.get_type_hints`, which `declared_type` uses: the annotation raised
  `NameError`, the declaration resolved to `None`, and `coerce_value` had no reason to
  call `parse_enum` — so `set_property("sourceEnvironment", "2")` stored `'2'` where
  the snapshot says `both`. The imports are now where the generator's own rule
  (`needs_runtime_import`, an enum default evaluated at class creation) always said
  they belonged: a one-time codemod moved them there — 978 imports in 481 modules over
  both slices — refusing an edge that would close an import cycle or redefine a name
  the module already binds, and was deleted once the tree had converged. The two sites
  a hoist cannot fix stay lazy and resolve through the getter's own import instead.
  `tests/unit/test_getter_annotations.py` holds the outcome: every column states a
  type, and for every column whose annotation resolves the declaration is that
  annotation.
- **A `timedelta` column held the ISO string.** Sixteen columns declare `timedelta` —
  `BookingAppointment.duration`, `ManagedAppProtection.period_before_pin_reset`,
  `LearningContent.duration` — and `_SCALAR_CONVERTERS` had no entry for it, so a read
  gave `'PT30M'`. `parse_duration` reads the ISO 8601 forms (`PT30M`, `P1DT2H`, `PT0S`,
  negatives) and `serialize_value` writes a `timedelta` back through `Duration.parse`,
  which no longer drops the seconds: 90 seconds was `PT1M` and is `PT1M30S`. A form with
  no `timedelta` equivalent — `P1M` names a month, not thirty days — is kept as the
  service sent it, like an unrecognized boolean.
- **A cyclic type's declaration was lost.** `ChatInfo` and
  `ConditionalAccessGrantControls` cannot be imported at module level — the edge would
  close an import cycle — so the getter imports them for itself, and `get_type_hints`
  saw a bare `NameError` where the module binds nothing. `declared_type` now re-reads
  the annotation with the getter's own imports: the source is parsed, not run, so
  learning what a getter declares never calls it. `OnlineMeeting.chatInfo` arrives as a
  `ChatInfo` instead of the dict the service sent, and `coerce_records` keeps the column
  instead of warning `Skipping unknown column 'chatInfo'`.
- **A column whose getter stated no type was a column the runtime could not read.**
  The last 120 — `Call.call_routes`, `SPActivityEntity.times`, `Field.indexed` — were
  hand-written getters whose only mention of a type was the fallback they passed to
  `properties.get`, and a fallback value is not a declaration. So
  `coerce_records(Call, [{"callRoutes": …}])` warned `Skipping unknown column
  'callRoutes'` and returned a record without it, and `set_property` stored the wire
  value verbatim. All 120 now state their return type, in 53 modules, taken from the
  CSDL property each getter reads (`Edm.String` → `str`, `Edm.DateTime` → `datetime`,
  `Collection(graph.callRoute)` → `ClientValueCollection[CallRoute]`) and checked
  against the default the getter builds. `Call.call_routes` is a
  `ClientValueCollection[CallRoute]` and `Field.indexed` a `bool` rather than the
  service's own text. Every one of the 13,205 columns `select_all()` returns now
  declares a type, and the next test pins it by name: the first getter that states
  none fails `test_every_column_states_the_type_it_holds`.
- **`SharingInformation.domain_restriction_settings` read the anonymous-link
  expiry.** The getter spelled `anonymousLinkExpirationRestrictionDays` — the name its
  neighbour already owns — so the domain restriction settings a sharing report carries
  were never read, and its own value was read as an `int`. It reads
  `domainRestrictionSettings` now, the name the CSDL gives it.

**Runtime**

- **The two retention feeds reject every query option they are offered.** A bare `GET
  security/triggerTypes/retentionEventTypes` is refused by Exchange's data-insights
  service before any option matters, and the same request with `$top`, `$skip`,
  `$orderby`, `$filter`, `$select` or `$count` answers 400 *"Query option 'Top' is not
  allowed. To allow it, set the 'AllowedQueryOptions' property on
  EnableQueryAttribute"* — an ASP.NET knob no client can turn. Both collections now
  declare the refusal with `@query_capabilities(...)`, so `.top(...)` and `.filter(...)`
  raise `QueryOptionNotSupportedError` with the documented reason instead of spending a
  round trip on a validation error that reads like a client bug.
- **The library imports on Python 3.11 again.** `TypeSchema` gave five `Mapping` fields
a `mappingproxy` instance as their dataclass default; 3.11 rejects an unhashable
default at class creation — 3.12 relaxed the check back to `list`/`dict`/`set` — so
`from office365.sharepoint.listitems.listitem import ListItem` raised `ValueError:
mutable default <class 'mappingproxy'> for field properties is not allowed`, and
with it every model, on a version `pyproject.toml` claims and that CI never ran.
The defaults are now `field(default_factory=...)`, the test matrix runs 3.10–3.13,
and `tests/unit/test_dataclass_field_defaults.py` fails on any interpreter when a
dataclass under `office365.runtime` defaults to an unhashable instance.
- **A throttled request waits the interval the service asked for.**
  `execute_query_retry` retried a `429`/`503` on its own backoff and ignored
  `Retry-After`, so the entry point the docs recommend for polite retries re-sent a
  throttled request at the worst moment, while the parallel paths honoured the
  header — the same library answering two ways. The default policy is now
  `Retry-After` with the backoff as fallback, and `max_delay` bounds *any* delay,
  so a caller's ceiling holds even when the service asks for an hour.
- **A timestamp with seven fractional digits is read on every supported
  interpreter.** `.NET` stamps carry seven, `datetime.fromisoformat` accepted more
  than six only from 3.11, so `parse_datetime` truncates and falls back to
  `fromisoformat` for the shapes the fixed format list does not spell — and
  `OperationStatus.last_action_date_time` no longer answers `None` on 3.10.
- **`to_json()` no longer emits `__`-prefixed bookkeeping** (`__etag`,
  `__deferred`, `__odata_type`): they describe the response, not the entity, and a
  plain-dict `to_json()` used to put them in a payload. `serialize_value` descends
  into a plain `dict`/`list`/`tuple`, so a hand-assembled payload is JSON-safe by
  construction rather than by `default=str`.
- **`DateTimeTimeZone.parse()` reads what callers pass.** A Graph `dict` raised
  `AttributeError` (so `EventCollection.add(start={...})` was unusable) and an
  aware `datetime` was flattened to UTC. It accepts a `datetime`, a Graph dict, a
  string or `None`, keeps a named zone, and emits Graph's documented wire form;
  `as_datetime()` reads the wall clock back, deliberately naive.
- `str()` on a scalar collection renders the list (`[freeBusyRead, read]`) where it
  used to print the internal type name, and `repr()` is quoted and type-qualified
  (`StringCollection([...])`); collection subclasses keep their own `__repr__`.
- **A limit prints what it measures.** A window that is a whole number of hours
  renders as hours (`200 requests / 24h`, not `/ 86,400s`), a byte budget prints as
  bytes wherever it appears (`150 MB / 300s`), a singular value takes a singular
  unit (`1 request`), and a line names its request type and the dimension it is
  counted against (`… (write on team, channel or chat)`).

**SharePoint (client)**

- **`List.export()` exports files.** The loop tested
  `item.file_system_object_type == FileSystemObjectType.File`, but the getter
  handed out the wire's number and `0 == FileSystemObjectType.File` is `False`, so
  every item was skipped.
- **A query bound to a subweb addresses the subweb.** `ClientQuery.url` pasted the
  query's own path onto the service root, so anything reached through a subweb read
  the root web's collection; the URL now derives from the bound object's own
  address.
- **`FeatureCollection.add(verify_if_activated=True)` activates a feature the
  collection does not list.** The guard asked `GetById('<guid>')`, which answers
  `{"d":{"GetById":null}}` at site scope even for an activated feature — and a dict
  holding one `None` is truthy, so it queued nothing. It now reads the collection
  the operation already fetches.
- **`Utility.resolve_principal_in_current_context` accepts its flags as enums:**
  `scopes` and `sources` are `Edm.Int32` bit flags, and the call sent the enum's
  repr, so every input came back `null`.
- **`SitePage.select_all()` is a projection the service accepts:** `TemplateScope`
  answers `400 NotSupported`, and a `$select` is all-or-nothing, so the type states
  the refusal in `_unselectable`.
- **A page's canvas is one property, not two.** `SitePage` declared
  `canvas_content` twice — a read-only twin shadowed the writable one, so
  `select_all()` could not name it and `odata_name("canvas_content")` raised. The
  duplicate is deleted, and a differential over `select_all()` names,
  `expand_all()` and a hydrated `to_json()` is byte-identical.
- **A copy job addresses its objects by absolute URL, and reports progress only for a real
  job.** `create_copy_jobs` wrapped `exportObjectUris` in the `{"results": [...]}` envelope
  the collection types serialize to, which the service rejects, and typed
  `CopyMigrationInfo.SourceListItemUniqueIds` as a plain list, so the ids it answered parsed
  to nothing — both round-trip now, and `get_copy_job_progress` takes the job
  `create_copy_jobs` returned instead of defaulting to an empty one: without it the service
  answers *"The copy or move job queue URI is not supported."* `CreateCopyJob` is retired
  server-side (*"obsoleted, please use CreateCopyJobs instead"*) and its docstring says so;
  `CopyJobProgress.JobState` is the `Edm.Int32` the service sends, not a string.
- Two endpoints that cannot work over REST say so: `UserProfilePropertiesForUser`
  is CSOM-only (`PeopleManager.get_user_profile_properties` is the reader), and
  `Tenant.get_site_subscription_id` raises `System.NotSupportedException`.

**Migration (client-side)**

- **The SharePoint assessment reads a list item's columns through the item**
  (`item.file_ref`, `is_file`, `has_unique_role_assignments`) instead of the JSON
  bag, through one named projection per load. A request-level differential over 252
  live assessment requests shows the widened projection as the only difference.
- **The list migration classifies a column once, through the column.** Five
  per-run caches over one `fields` read are replaced by `_source_fields()` and the
  column's own predicates, and the target reads the same ones, so the two halves of
  the pipeline can no longer disagree about what a column is. Both `$select` lists
  are byte-identical.
- **A file's current version no longer appears twice in its history.**
  `File.Versions` includes the current version and the read passed it through as an
  older one, so the ordinary case (current version is the newest label) listed that
  label twice in `Manifest.xml`.
- **A plain list is no longer routed to the server-side package.** `Manifest.xml`
  has no `<List>` object, so a list record became a `<File>` whose content was the
  record's `dict` repr, silently; a list task now falls back to the REST adapters
  and says so, and the package target refuses any item that is not a file or a
  folder.
- A replayed view is created with the columns the target list has, and the drop is
  reported rather than failing the whole replay with
  `Column 'LinkTitle' does not exist`.
- A re-run of `configure()` writes nothing, and whatever a structure replay cannot
  reproduce is reported on `target.warnings` instead of assumed.

**Migration (server-side package path)**

- **A resumed package run re-attaches to the job it already submitted.** The job id
  lived only in memory, so the runner's resume drove `commit()` again and submitted a
  *second* ingestion job for the same package: the service ingests the same content
  twice, and neither job's outcome is attributable to a run. The id is now recorded
  with the package's paperwork — `FileSystemStaging` writes `job.json` beside
  `Manifest.xml`, `BlobStaging` uploads the same record (encrypted) to the manifest
  container — and `commit()` adopts it instead of submitting, unless
  `resubmit=True` says the recorded job is known-failed. The record names its
  destination (web id + list title), so a second library reusing the directory does
  not adopt the first one's job.

**Migration (Outlook)**

- **Calendar and contact exports derive their projection from the model**
  (`Event.select_all()` / `Contact.select_all()`). The hand-kept list omitted
  `isCancelled`, which the export filters on — and `$select` answers only the names
  it lists — so a cancelled event was exported with `is_cancelled: false`.
- **`iCalUId` is read as the service spells it.** The envelope asked
  `get_property("iCalUid")` — one capital short — so every sidecar carried
  `"ical_uid": null` and the `.ics` `UID` fell back to the tenant-local Graph id
  instead of the identifier other calendar clients match on.
- A recurring event's sidecar carries JSON, not `repr` text: `recurrence` is
  flattened through `to_json()` instead of reaching `json.dumps` as a typed value,
  which no import could replay.
- **Verification compares in the source's timezone.** Exchange renders times in the
  signed-in mailbox's zone, so a migration into a differently-zoned mailbox
  reported every event as a mismatch while the instants were identical; the read
  now asks for the item's own zone with `Prefer: outlook.timezone`
  (`prefer_outlook_timezone`).

**Permissions**

- **Three live suites were skipped for a licence the tenant already had.** They declared four
  retail E5 SKU part numbers and nothing else, and a SKU part number is packaging rather than
  capability: the test user's seat is `DEVELOPERPACK_E5`, a developer pack that carries
  `RECORDS_MANAGEMENT` and `PURVIEW_DISCOVERY` (both `Success`), so the licence group answered
  "not licensed" for a user who could make every call and 13 tests never ran. The licence fact
  now reads `me/licenseDetails` for the SKU part number *and* the service plans inside it, and
  the marker names the plan. Same rule as the catalog: declare the fact the call depends on, not
  the label it is usually sold under.
- **The preflight report dropped a whole flow instead of resolving it.** A requirement was
  looked up with a client built for the auth flow the suite uses, and `--verify` could build
  one only for the password and secret flows: every SharePoint suite signs in with the
  certificate, so its requirements came out "unverified" and a report of what a tenant grants
  said nothing about the package that owes 2,238 declarations. The same certificate is a
  Graph credential, so the report now signs in with it and asks the app that will run the
  tests. Measured on the tenant: 3 unverified rows became 3 met.
- **`ServicePrincipal.get_application_permissions` reported a subset of the client's
  grants.** It read the resource's `appRoleAssignedTo` navigation property, which was
  expanded into the request; Graph answers an expanded collection with one truncated
  page. Measured on a tenant where the client app holds 43 application permissions on
  Microsoft Graph: `$expand=appRoleAssignedTo` returned 21, the paged collections
  returned 44 assignments (43 of them the client's, 43 distinct roles, set-equal to the
  43 `roles` in its token). Every reader believed the truncated answer — a skip decision
  in a live test, a permission report, and the "already granted" check that makes
  granting idempotent. `appRoleAssignedTo` accepts no `$filter` at all (`principalId`
  answers `Links to EntitlementGrant are not supported between specified entities`,
  `appRoleId` answers `Invalid filter clause appRoleId: System.Guid`), so the reader now
  asks the same relationship from the client's side — paged
  `servicePrincipals/{client}/appRoleAssignments`, filtered by `resourceId`. Measured
  after: 43 of 43.
- **`ServicePrincipal.grant_application_permissions` granted twice.** Its idempotency
  check read the same truncated collection, so a role the client already held was
  posted again; Graph rejects the duplicate and the caller saw a `ClientRequestException`
  it could only read as a missing `AppRoleAssignment.ReadWrite.All` scope. Granting and
  revoking now read the assignment list the reader above reads.
- **`ServicePrincipal.get_delegated_permissions` answered from one grant.** It took
  `next(g for g in grants if g.resource_id == self.id)` and split that grant's `scope`,
  so a resource holding a tenant-wide grant plus per-user ones reported only the first
  one found. It reads every grant for the resource now, and takes `consent_type`
  (`"AllPrincipals"` by default, `"Principal"`, or `None` for both) rather than
  silently mixing two different facts — a per-user consent makes a call work for that
  user alone. Measured on the same tenant: 47 tenant-wide scopes, 2 per-user scopes
  (`User.Read.All`, `UserAuthenticationMethod.ReadWrite`), 49 for both.
- `ServicePrincipal.revoke_delegated_permissions` removes the scope from grants on *this*
  resource only. It deleted every grant of the client app whose `scope` mentioned the
  name, including grants on other resources that happen to spell it the same way
  (`Mail.Send` is granted separately on Graph and on Exchange Online).
- **Ten application permissions were declared that Microsoft Graph does not publish.** The
  first thing the catalog did was disagree with the tree: the eight workbook methods that open,
  refresh and close an Excel session and the two `/search/query` methods named `Files.ReadWrite`
  and `People.Read` for the *application* flow, where Graph publishes only `Files.ReadWrite.All`
  and `People.Read.All` — the delegated names are real, so nothing looked wrong. A declaration
  of a name the API does not publish cannot be granted, cannot be satisfied by a token, and
  cannot be refused by a live test in a way that reads as an error, so the wrong name was
  invisible; `--grant` would have failed on it, and the preflight line named a permission that
  does not exist. Both now name the published form.
- **A live suite named a permission Microsoft Graph does not publish, and `--grant` died on
  it.** `tests/directory/test_governance.py` listed `Approve.AppConsentRequests.Read.All`
  beside `EntitlementManagement.Read.All` as an any-of, which is harmless while the group is
  merely read: the second name answers. Granting it is where it stopped being harmless — the
  directory accepts any string, so the planner asked for it, and `app_roles[...]` answered
  `KeyError` from inside a response listener, which aborted the whole pass after two grants
  and reported nothing about the other forty. Three changes: the marker names the one
  permission that exists; `grant_plan` prefers a name its API publishes and keeps an
  unpublished one only when a group offers nothing else, so the group stays visible instead
  of vanishing; and `apply_plan` reports a name the API does not publish instead of
  attempting it — a recorded grant for such a name is one the token never carries, which the
  next `verify` would call met. `AppRoleCollection.__getitem__` now says what it looked for
  (`this API publishes no app role named 'Approve.AppConsentRequests.Read.All'`) rather than
  raising the bare key from a listener, where it read as a crash with no subject.

## [3.3.0] - 2026-10-18

Two stories: the SharePoint migration layer grew from "copy items" to a resumable,
verifiable site copy, and the runtime grew async/await, long-running operations and
a set of write/lookup primitives that the generated surface lacked.

### Breaking in 3.3.0

The public surface is additive; three modules moved, and the old import paths are
gone. Nothing else in this release changes or removes an existing API.

- `Report` calls return the new `ReportResult` (a `ClientResult` subclass, so
  `.value`, `bytes()` and `.execute_query()` behave as before) instead of
  `ClientResult[bytes]`.
- The Security API lives at `office365.security` (was
  `office365.discovery.security`).
- `TaskStatus` lives at `office365.todo.tasks.taskstatus` (was
  `office365.todo.taskstatus`).

### Added

**SharePoint migration**

- **Whole-site (same-tenant) migration.** `MigrationSession.add_site_task(...)`
  resolves a `migrate_all` task into one job per list — each with its own manifest
  and checkpoint — creating missing target containers and replaying each list's
  structure (columns, content types, views, container settings) before content is
  copied. `include_subwebs=True` mirrors the source subsite tree.
- **A run that names what it is copying.** The `migrate_site.py` console prints a
  heartbeat per list (`[ 4/24] Documents  migrating  412/1,010 (40.8%)  9.7 it/s  ETA
  1m02s`) and a closing line the moment a list finishes (`✓ [ 4/24] Documents  1,010
  copied  1m42s  9.9 it/s  2.4 MB/s`, `!` when it left failures); progress counters
  are derived per job in both serial and parallel mode (a carried-over rate and total
  no longer produce an ETA of hours), the window restarts when the stage changes, a
  heartbeat carries its `subject`, and repeated warnings print once with a count.
- **Several lists at once, and both phases reported.**
  `MigrationSession.start(concurrency=N)` runs `N` list jobs in parallel, each on a
  `ClientContext` clone that shares the auth context, transport and `RateLimiter`
  (adapters are re-addressed with `rebind()`, since a context owns one
  pending-query queue); `add_site_task(progress=...)` heartbeats the resolution
  phase (`lists`, `containers`, `structure`, then `pages`/`navigation`/`branding`)
  instead of staying silent. Example flag: `--lists-in-flight N`.
- **Throttling as a measured number.** `ThrottleMonitor` counts responses,
  `429`/`503`s and the `Retry-After` seconds a run waited for (observation only:
  retry, backoff and pacing are untouched); `MigrationSession(throttle=...)` logs
  `throttled` events and adds the totals to `run.completed`. Example flag:
  `--pace SECONDS`, the proactive lever.
- **Web scope, not only lists.** Branding (master page, theme, logo, rebased asset
  URLs), `Title`/`Description`, custom permission levels, web role assignments,
  Quick Launch and top navigation, the home-page designation, and modern site
  pages plus classic wiki pages are copied. Workflows, InfoPath forms, BCS
  external lists, checked-out files and un-published (minor) versions cannot be
  produced by a client-side copy, so each is reported instead.
- **Site-scope honesty.** The features (publishing, records management, document
  id) and regional settings a copy never replays are compared and reported, and
  one verification report answers "did this web migrate?" across content,
  structure, settings, pages and security.
- **Structure fidelity.** Column and view formatting JSON, taxonomy
  (`TaxonomyFieldType`/`…Multi`) values, multi-choice, hyperlink, multi-value
  lookup and person remapping, a content-type identity map (SharePoint assigns
  recreated types fresh ids), folder item metadata, list container settings with
  approval state, and attribute-level column verification (`Required`, `Indexed`,
  choices, validation).
- **Delta re-runs name the drift** a copy cannot reconcile: a source deletion
  leaves a target orphan, a rename or move looks like a new item.
- **Record-list fidelity hooks** (timestamps, authorship, unique permissions),
  matching what the document-library adapters already did.

**Runtime**

- **Async/await across the query API:** `execute_query_async`,
  `execute_query_async_retry`, `execute_query_parallel_async` (with an `on_error`
  collector), `execute_batch_async`, `get_all_async`, `export_to_async`,
  `retry_async`, async `beforeExecute`, `RateLimiter.acquire_async`/`paced_async`,
  an abort path that cancels in-flight siblings, `contextvars` preserved across the
  offloaded call, a tunable offload pool, and an optional native-async
  `HttpxTransport` (`[httpx]` extra).
- **Streaming and large data:** `BaseTransport.stream`/`stream_async`,
  `File.download_session`/`download_session_async` and `DriveItem` content streams,
  `DriveItem.resumable_upload_async`, bounded-memory `export_to`, high-level
  `Folder.download` / `FileCollection.download`.
- **Long-running operations (LRO):** a transport-agnostic `OperationPoller`
  (Operation-Location / Azure-AsyncOperation / `Retry-After`, terminal states,
  continuation tokens, cancel + timeout + progress hook), the `PollableOperation`
  mixin, `LongRunningOperationResult`, `Prefer: respond-async` helpers,
  `TeamsAsyncOperation.poll_for_status_async`, streamed report export, and
  awaitable `MigrationServerJob.monitor_async`/`progress_async`/`errors_async`.
- **Write primitives:** a unified `EntityCollection.upsert` (idempotent
  create-or-reconcile), `EntityCollection.update_all`, `Entity.update_properties`,
  `Entity.delete_object(ignore_missing=True)`, `List.ensure_field`/`ensure_fields`,
  `Field.schema_xml_for_copy()`, batch `$batch` writes, and token-aware
  `Web.get_securable_object`.
- **Best-effort batches:** `ClientRuntimeContext.collect_batch_failures()` runs a
  batch tolerantly — a rejected sub-request (denied write, validation error,
  retries exhausted) is recorded against its own query as `(query, exception)` and
  the remaining sub-requests still execute, instead of the first failure aborting
  the whole batch. Throttled sub-requests are still retried, and the default
  outside the scope is unchanged (first failure raises).
- **Lookups:** one rule for `get_by_*` (resolve one) versus `find_by_*` (return
  `None`), tolerant Graph resolvers, `ClientObject.get_or_none()`, and a bounded
  `single()`.
- **Query capabilities:** declarative `@query_capabilities(...)` with
  property-level `Prefer` injection, and a
  `Prefer: include-unknown-enum-members` helper.
- **Auth and identity:** `ClientRuntimeContext.with_auto_retry(...)` (inherited by
  clones), async token locks and `HttpxTransport` clients that follow the running
  event loop (a transport reused from a second `asyncio.run()` rebuilt its
  `AsyncClient`; a lock bound to a finished loop is replaced), a typed
  `AccessDeniedException` for 401/403, `@require_permission`
  hints on denied requests, `Credential.is_expired`/`days_until_expiry`/
  `expiry_status`, idempotent `Application.ensure_certificate`,
  `with_certificate(public_certificate=...)` without a thumbprint, idempotent app +
  service-principal setup and application-permission grants, async token
  callbacks, and `Sites.Selected` helpers (`Site.grant_access`).
- **Smaller surface:** `client.domains` as a `DomainCollection`,
  `RestorePointCollection` with a typed `search`, `PlannerTask.assign_to` plus
  checklists, `NotebookCollection.ensure`, OneNote pages from in-memory HTML,
  `ReportResult.to_text()`/`csv_rows()`, `AttachmentBase.content_bytes`,
  readable `__str__`/`__repr__` for runtime objects, and term-store hierarchy
  export/import without the payload name clash.

### Changed

- `verify()` reports unexpected target items as such (a new
  `VerificationReport` field) instead of as content mismatches.
- Planner writes derive from `PlannerEntity`: `If-Match` from the latest etag plus
  `Prefer: return=representation`, so consecutive updates no longer fail with a
  stale-token `409`.
- Twelve duplicate model modules re-export the canonical class, and
  `ViewCollection.create`/`ensure_view` annotate `view_type` as `int | str`. (The
  three moved modules are listed under *Breaking in 3.3.0*.)

### Fixed

**Migration (client-side)**

- Item values: hyperlink columns, multi-choice columns, multi-value
  `Lookup`/`Person` (including the `Type="Lookup" Mult="TRUE"` spelling),
  taxonomy, and `ListItem.set_property` on multi-person columns are all migrated;
  bulk creates adopt the list's entity-type annotation; an empty multi-value
  column no longer fails verification.
- Item ACLs: an empty ACL, a double inheritance break and a false mismatch are
  handled; fidelity writes are applied in order (permissions, authorship,
  timestamps) and folded into one system update, so they no longer create
  versions and the exact instant is restored on both list and document items.
- Preserved runs: authorship sent its own `ValidateUpdateListItem` and the
  timestamp write then repeated the same values, so every preserved item cost two
  system updates (three with approval state). The principals are resolved and
  cached first and written **once** — with the timestamps when they are preserved,
  otherwise in a single final write before the approval step.
- Record lists: content is verified instead of reported `unverifiable`, writes
  flush and checkpoint per chunk, and `conflict_resolution=OVERWRITE` now reaches
  record targets.
- Document libraries: folders are created as folders (they were uploaded as
  files), SharePoint's own `Forms/` scaffolding and the auto-provisioned
  `SiteAssets/<web title> Notebook` are skipped rather than reported as extra
  items, folder system metadata and column values are written, approval state is
  carried, and Office Open XML documents are no longer flagged as content
  mismatches (SharePoint re-serializes them, so byte equality is unattainable).
- Warnings: structure provisioning logged each note at `warning` (one of them with
  the list name prefixed) *and* handed it to `session.warnings()`, so every note
  printed twice — once by logging's last-resort handler, once by the caller. They are
  `DEBUG` provenance now; the caller decides how to show them.
- List settings: the differing container settings (versioning, moderation,
  version limits, check-out, item-level read/write policy) are applied in one
  `$batch` instead of one request each. A change set is atomic, so a refusal falls
  back to writing them one by one — a setting the list type cannot accept is still
  its own warning and does not abort the others.
- Structure: content-type field links skip built-in and SharePoint-owned columns,
  a nameless content type no longer sends a null name, `ContentType.set_default`
  works, `reorder_fields` sends a plain JSON array, `FieldLink.field_internal_name`
  falls back to `Name`, `ContentTypeId` declares the right OData type, V3 enums
  serialize as `Edm.Int32`, and the taxonomy `TextField` round-trips.
- Structure replay: a list's content-type field links are read, added and read
  back in `$batch` rounds under `collect_batch_failures()`, so one round of three
  requests replaces the one-per-link exchange that dominated a replay (~35 requests
  for a ten-column, five-view list, ~60 % of them links). A refused column is still
  reported per column with the server's reason, and the read-back — not the
  sub-responses — decides what is linked, because a change set is atomic and one
  refusal rolls its siblings back while they answer `200`. Link order is restored
  per content type only when the target's order differs, so a re-run writes
  nothing.
- Site: a re-run no longer mints `Home-2.aspx`/`Home-3.aspx`, `ClientContext.clone(url)`
  no longer sends requests to the original site, a `select` projection no longer
  drops every item value and attachment, manifest/checkpoint saves create their
  directory and are crash-safe, a stale error handler no longer swallows later
  failures, and structure-provisioning warnings reach `session.warnings()`.

**Migration (server-side package path)**

- Authors and ACLs take effect (`PermissionEntry` carries the system id, display
  name, e-mail and role masks; `MigrationItem` carries author/editor), version
  history is carried through `MigrationJob`, timestamps are emitted as valid XML
  `dateTime`, a single-list task no longer skips structure replay, `CreateFieldAsXml`
  field links are emitted, and `UserGroup.xml` writes a normalized PUID.

**Runtime and models**

- Generated Graph enums sent their CSDL ordinal instead of the wire value — the
  model now carries the member name. Two models declared the wrong OData type name,
  the generator could write into hand-written files, and a forced regeneration
  re-declared inherited dataclass fields.
- Payloads: `datetime`/`date`/`Enum`/`UUID` scalars in dict- and list-built bodies,
  reserved-word property declarations, and the concrete OData type for Teams
  members, chats (topic) and shared channels, To Do attachments and links, URL
  threat assessments, subject-rights `dataSubject`, change notifications, Intune
  role assignments, and Planner assignment/checklist maps.
- Transports and batching: a thread-safe default `RequestsTransport`,
  transport-level TLS verification and proxies, `httpx` per-request `NO_TIMEOUT`,
  batch GETs placed outside the change set, multi-phase SharePoint batch writes,
  and list-item creates *and updates* deferred until the list's entity type is
  known (a batched hyperlink or multi-value update used to be sent unannotated and
  rejected with `A value without a type name was found`).
- Small ones: `ReportResult` raw content, `Group.created_datetime` returning `None`,
  nested OneDrive folder addressing, `ensure_folder`/`ensure_file` on a folder
  addressed by id, sharing-link expiration dates, webhook expiration format,
  `$top` sent to `directoryRoles`, sign-in timestamps as `datetime`, doubled
  apostrophes in OData literals, certificate reuse detection in the setup scripts,
  naive credential timestamps, `has_application_permissions` false negatives,
  agreement-file inheritance, the device-flow prompt, chat members right after
  creation, and `examples/onedrive/termstore/export_tree.py`.
- `SearchService.post_query` accepts `sort_list` (a list of `Sort`), the same
  argument the GET form `query` takes; it is sent in the request body as
  `SortList`. A POST that asks for no sorting sends the same body as before.

### Deprecated

- The collection-resolving `get_by_name` / `get_by_title` / `get_by_path` helpers
  emit a `FutureWarning`; `get_by_*` now means "resolve one", `find_by_*` means
  "return `None`". Removal in v4.

### Removed

- `SubjectRightsRequestIdentity`, the unused `MigrationMode` enum, and three stale
  duplicate model modules.

### Documentation

- New guides: `docs/migration.md` (plan → copy → verify, with the limits stated),
  `docs/async.md`, `docs/long-running-operations.md`, and an async section in the
  README and the docs reading path.
- The example galleries are now lifecycle- or resource-guided tours around a
  `quickstart.py` each: SharePoint getting-started, Teams, usage reports, Microsoft
  To Do, Intune (with a lifecycle diagram) and Purview, plus an async example
  catalog.

### Internal

- Developer onboarding reworked: credentials flow through `tests/settings.py` and
  `.env`, `python -m tests.setup` guides the setup, `tests/doctor --require` checks
  a run's prerequisites, `applications/rotate_cert.py --generate` mints a
  self-signed certificate, and `OFFICE365_USERNAME` / `OFFICE365_USERNAME_ALT`
  replace the two-user test model.
- `--log-level DEBUG` in the migration example now prints the run's events as
  plain lines (`configure_text_logging()`), instead of being a no-op without
  `--log-json`.

## [3.2.0] - 2026-09-27

### Added
- **Locked-file handling (HTTP 423):** typed `FileLockedException` (also
  `SPFileLockedException`) parses the lock holder into `.lock_owner` with remediation
  in `.GUIDANCE`; `retry_on(FileLockedException)` opts into retrying lock errors, and
  `delete_object(bypass_shared_lock=True)` sends `Prefer: bypass-shared-lock` on
  Graph and SharePoint. See `examples/sharepoint/files/handle_locked_file.py`.
- **Idempotent file provisioning:** `DriveItem.ensure_file(path, content,
  on_conflict=...)` reuses or overwrites the leaf file, creating missing parents.
- **Typed CAML query builder:** `Caml` / `CamlQuery.builder()` build `ViewXml` from
  composable expressions (comparisons, field-typed helpers, `Caml.now`, logical joins
  rendering binary-nested CAML, `where/order_by/group_by/row_limit/scope/view_fields`);
  raw `ViewXml`/`parse` remain. New modules under
  `office365/sharepoint/listitems/caml/`.
- `ImportResult` — a deferred, source-agnostic streaming import driver with a
  sequential, batch, or iterated terminal; `ClientObjectCollection.import_records()`
  and `List.from_dataframe()`.
- **Idempotent list imports:** `List.import_dataframe(..., key=..., key_field=...,
  on_conflict="skip"|"upsert")` derives SHA-256 keys and skips/updates existing rows
  (`ImportStats.skipped`, `enforce_unique`, `dry_run`).
- **Resumable imports:** `ImportResult(checkpoint=...)` persists the committed cursor
  per chunk; `resumed_from`/`checkpoint`/`ImportStats.resumed_from` expose the offset;
  `on_error="collect"` records a failing chunk and continues.
- `ClientObjectCollection.clear()` and a `concurrency` argument on
  `Entity.execute_batch()`.
- `OperationStats` shared counter base, specialized by `ImportStats`/`MigrationStats`.
- **Live import progress:** `progress` fires immediately (with the resumed offset),
  per committed chunk, and per completed batch; `run_parallel` reports on the calling
  thread; `execute_batch`'s `success_callback` fires per batch in sequential mode;
  `List.import_from(..., total=...)`.
- **Best-effort migration fidelity:** `preserve_timestamps`/`preserve_permissions`
  applied client-side via `DataSource.read_permissions`, `DataTarget.apply_timestamps`
  and `apply_permissions(item, permissions)` (`PermissionEntry`).
- **Migration guide:** `docs/migration.md`.
- **Server-side migration (full fidelity):** `Site.provision_migration_containers`,
  `provision_migration_queue`, `create_migration_job_encrypted`, and
  `get_migration_job_progress`; `MigrationServerJob.submit_encrypted`/`progress`/
  `status_fn`; `parse_progress_events`.
- **Migration API package layer** (`office365.migration.package`): models for
  `Manifest.xml`/`ExportSettings.xml`/`SystemData.xml`/`UserGroupMap.xml`,
  `PackageBuilder`, `FileSystemStaging`, `BlobStaging` (new `[azure]` extra),
  `create_staging(...)`, and `SharePointPackageTarget`. Covers the document-library
  subset; the generated XML is not yet live-verified.
- **Storage & vendor-neutrality docs:** `docs/migration.md` covers which legs need
  Azure, the `Staging` seam, and a step-by-step example.
- **Encrypted migration staging:** `BlobStaging`/`create_staging` accept an
  `encryption_key` (AES-256-CBC, unique IV); `SharePointPackageTarget` forwards it,
  and `[azure]` now also pulls in `cryptography`.
- **Migration examples:** `migrate_library_serverside.py` and the tenant-free
  `package_library.py`.
- **SPMT-style migration sessions:** `MigrationSession` mirrors the SPMT cmdlets
  (`register`/`get`/`add_task`/`remove_task`/`show`/`start`/`stop`/`unregister`), with
  `MigrationSettings`, `MigrationTask`, and a SharePoint resolver (client-side REST or
  `use_migration_api=True`); `MigrationOptions` gained `created_after`/`modified_after`.
- **`FileVersions` scan** — records files with version history, with the SMAT columns.
- **SMAT report scans:** `CheckedOutFiles`, `LargeExcelFiles`, `BrowserFileHandling`,
  `LongOneDriveUrls`, `ThicketFolder`, and `UnsupportedSiteTemplates`, sharing a
  `SiteScanRecord` base; `WebTemplateType` covers the full `Get-SpoWebTemplate`
  catalog; `Limits.LARGE_EXCEL_FILE` backs the Excel threshold.
- **Locale-independent error classification + SharePoint taxonomy:** deterministic
  `MATCH_PRIORITY` dispatch; `ClientRequestException.hresult`/`.error_type`; a
  `SharePointException` catch-all plus typed `SPFileCheckOutException`,
  `SPListDataValidationException`, `SPFieldValidationException`,
  `SPFieldValueException`, `SPDuplicateValuesFoundException`,
  `SPInvalidLookupValuesException`, `SPContentTypeReadOnlyException`, and
  `SPContentTypeSealedException`.

### Changed
- **Error classification is locale-independent:** exceptions key off the numeric
  HRESULT and/or embedded .NET type name; HTTP 423 disambiguates
  `SPFileCheckOutException` from the shared-lock `FileLockedException` (an unresolved
  423 still maps to `FileLockedException`).
- **Data-pipeline naming (breaking):** `from_*` is the streaming entry (returns
  `ImportResult`) and `queue_*` the deferred path. Removed `import_from`/
  `import_records`/`import_dataframe`/`import_from_file` and `to_json_file`/
  `from_json_file`; `FieldCollection.from_dataframe` → `ensure_from_dataframe`.
- **Architecture:** the data-interchange surface moved onto a new `RecordCollection`
  base (inherited by every typed `EntityCollection`); formats resolve through
  `runtime.converters.registry`; keyed skip/upsert is a pluggable `UpsertTarget`
  implemented by `ListItemUpsertTarget`.
- `import_from`/`import_records` gained `enforce_unique=True` and `dry_run=True`.
- `List` gained record facades (`import_from`/`import_dataframe`/`import_records`,
  `export_to`/`to_dataframe`); `List.from_dataframe` is now deferred.
- `SharePointListSource` reuses the shared record projection.
- `MigrationOptions.preserve_timestamps` defaults to `False`; unhonorable flags raise
  `NotImplementedError`; `preserve_versions` still needs the server-side Migration API.
- `Site.create_migration_ingestion_job` — `azure_queue_report_uri`/`ingestion_task_key`
  are now optional.
- **Streaming export + row-level dead-letter:** `export_to(..., page_size=...)` streams
  appendable formats; with `on_error="collect"` and a `dead_letter`, each failing row
  is dead-lettered.
- **Large-list threshold mitigations:** typed `SPQueryThrottledException`; paged
  `Folder.get_files` (refs #930/#936/#462) and `List.get_items(query, page_size=...)`;
  `List.ensure_indexed`/`Field.ensure_indexed` (the real fix for #427); a warning on
  unpaged filter/sort queries; new `docs/large-lists.md` (including #726).
- **Large-list UX:** list-view collections (`ListItemCollection`, `FileCollection`,
  `FolderCollection`) warn once at the 5,000-item threshold (refs #930/#936);
  `CamlQuery.index_candidates`/`List.index_candidates`; `List.check_query` pre-flights
  a query.
- **Migration-parity vocabulary:** `ImportResult.run(...)` aliases `execute_batch`;
  `ImportResult.verify`; a shared `VerificationReport` (`runtime.verification`).
- **More formats + path/IO parity:** `tsv`, `parquet`, `orc` and `feather`
  (`[parquet]`), `from_sql`/`to_sql` (`[sql]`), `from_duckdb`/`to_duckdb`
  (`[duckdb]`); every reader/writer accepts a path, `PathLike`, or open file.
- **DataFrame ⇄ SharePoint file bridge:** `Folder.write_dataframe`/`File.write_dataframe`,
  `Folder.read_dataframe`/`File.read_dataframe`, and `List.from_file`; codecs are
  `dataframe_to_bytes`/`dataframe_from_bytes`.
- **Typed field mapping on import:** `List.import_from(..., schema={column: FieldType})`
  coerces values into the payload shape; `coerce_field_value`; generic
  `RecordCollection.import_from(..., coerce={key: converter})`.
- **Column mapping:** `import_from(..., mapping={...})` renames source columns/keys.
- **Import verification:** `RecordCollection.verify_keys(keys)` and
  `List.verify_dataframe(df, key=...)`.
- **Dead-letter capture:** `import_from(..., dead_letter="dl.jsonl")` appends each
  collected chunk failure.
- **Import schema evolution:** `List.import_from(..., on_schema_change="evolve"|"fail")`,
  backed by an `ImportResult` `before_chunk` hook.
- **Incremental migration watermark:** `MigrationRunner` uses the persisted
  `Checkpoint.source_watermark` to skip and advance.
- Removed `office365/migration/_util.py`; helpers moved to `runtime.operations`,
  `runtime.converters.scalars`, and `runtime.converters.json_file`. Report writing is
  now per-format (`write_dataset`/`write_formats`).
- `MigrationItem` carries `created` and `author_id`/`editor_id`.
- **Idempotent metadata:** all client-side `ensure_*` share
  `runtime.queries.get_or_create.get_or_create`/`create_or_get` and accept
  `on_conflict="skip"|"update"`.
- `List.ensure_field`/`ensure_fields` and `FieldCollection.from_dataframe` now return
  the ensured entities; `List.ensure_fields_from_dataframe` was removed.
- **Breaking:** `List.from_dataframe()` returns an `ImportResult` driver; `progress`
  is keyword-only.
- The SharePoint list migration target flushes and discards each chunk.

### Fixed
- **Collection-bound OData operations are no longer generated onto item types.** A
  bindable `FunctionImport` whose `this` is `Collection(X)` was attached to item class
  `X`; the SharePoint (v3) and Graph (v4) readers now skip them, removing 49 methods
  from 24 item classes (e.g. `User.remove_by_id`, `Feature.remove`, `SubtitleFile.add`,
  `SitePublishingPage.set_multilingual`, `SiteProperties.get_lock_state_by_id`,
  `MigrationTask.batch_*`).
- **A custom session carrying its own auth handler now counts as credentials (refs #1045).**
  SharePoint requests (and the form-digest and batch paths) skip
  `AuthenticationContext.authenticate_request` when the transport carries a handler
  and nothing is configured.
- **Server-side file imports need a matching `SPListItem` (live-validated).** The
  Migration API silently skips an `SPFile` unless the package also contains its
  `SPListItem`; `PackageBuilder.add_file` now emits it. Every `<User>` must carry
  `SystemId`, and `DeploymentRoles` must not be emitted.
- **`PackageBuilder.add_role_assignment` now defaults `object_type="2"`.** The grant
  itself and `Author`/`ModifiedBy` still don't land (the target SID isn't exposed by
  the SPO REST API; parked).
- **On-prem NTLM auth works again (refs #1045).** `ClientContext(url, allow_ntlm=True)`
  delegates to `AuthenticationContext.with_credentials` and forwards
  `allow_ntlm`/`browser_mode`; the retired-SAML guard still fires for SharePoint Online.
- **`SharePointPackageTarget` no longer emits an empty `ExportSettings` `SiteUrl`.**
  It resolves the site URL or raises a clear error, and accepts a `source_type`.
- **`Manifest.xml` now matches the service shape.** It emits the library root
  `SPFolder`, the `SPDocumentLibrary`, a folder per subfolder and an `SPFile` per file;
  `UserGroupMap.xml` → `UserGroup.xml`; the `ViewFormsList` namespace is fixed.
- **Migration packages now emit the manifest files the API fetches** (`Requirements.xml`,
  `RootObjectMap.xml`, `LookupListMap.xml`, `ViewFormsList.xml`). Failed jobs are
  diagnosable via `MigrationServerJob.all_events`/`errors` and
  `SharePointPackageTarget.events`/`errors`/`diagnose`.
- **`CreateMigrationJobEncrypted` sends the AES key as base64 text** instead of
  decoding it.
- **`$skip` paging no longer collides with a server `$skiptoken`.**
- **Idempotent imports load existing keys on every run**, and `ImportCheckpoint` now
  records a source signature so a mismatch rescans the source.
- DataFrame import no longer silently drops a column colliding with a built-in field
  (it is imported with a `_` suffix and a warning).
- `series_kind`/`field_type_from_kind` handle more kinds and fall back to `Text`
  instead of raising `KeyError`.

## [3.1.1] - 2026-09-13

### Fixed
- SharePoint form digest is cached correctly again (`_valid_from` set on fetch,
  safety-margin refresh), so `/_api/contextInfo` is fetched once per site/run and
  pre-warmed before parallel `execute_batch`.
- A throttled digest refresh (`429`/`503`) is retried honoring `Retry-After`, and an
  expired/invalidated digest (`403`) is refreshed and retried once, surfaced as
  `SecurityValidationException`.
- Whole-batch throttling (`429`/`503`) honors `Retry-After` instead of exponential
  backoff.
- `File.open_binary`/`File.save_binary` no longer percent-encode the whole OData call
  ([#978](https://github.com/vgrem/office365-rest-python-client/issues/978)); only the
  path value is encoded.

## [3.1.0] - 2026-09-13

### Added
- **Migration toolkit** — product-agnostic core plus `sharepoint`, `outlook` and
  `teams`: resumable `MigrationJob`/`MigrationSession`, filesystem/SharePoint/JSON/
  Teams archive adapters, parallel transfer, a server-side ingestion job, and
  summary/item/failure reports.
- **SMAT-style pre-migration assessment** — modular scans/containers,
  `MigrationAssessor`/`MigrationTenantAssessor`/`MailboxAssessor`, typed reports
  (`LargeSites`, `LockedSites`, `MailFolders`), and CSV/JSON export.
- **Parallel execution** — `execute_batch(concurrency=N)` on `ClientContext` and
  `GraphClient`, plus `execute_query_parallel(concurrency=N)`; per-request retry
  honoring `Retry-After`.
- **Data pipeline** — CSV/JSON/NDJSON/Excel import-export, `from_csv`/`from_json`/
  `from_records`, dynamic list-item columns, and an optional pandas bridge.
- **SharePoint** — taxonomy term store (OData v2.1/V4), site primitives, folder
  download with version history, zip ↔ folder primitives, `Web.ensure_list`,
  `DriveItem.ensure_folder`, and typed field creators.
- **Generator** — OData function/action generation, a return-type descriptor/resolver,
  and list-typed primitive collection parameters.

### Changed
- Thread-safe auth and form-digest caches (single-flight refresh);
  `ClientContext.clone` shares the auth context and transport.
- First-class retry (exponential backoff + jitter) and throttling primitives;
  `ClientQuery` generics made consistent.
- Examples reorganized into product galleries and an SPMT-style migration flow
  (`assess/` → `migrate/` → `monitor/`).

### Fixed
- Long file paths in moves ([#988](https://github.com/vgrem/office365-rest-python-client/issues/988)) —
  body-based `File.move_by_path`/`MoveCopyUtil.move_file_by_path`; slashes are no
  longer percent-encoded inside OData string literals.
- Bulk OneDrive downloads ([#881](https://github.com/vgrem/office365-rest-python-client/issues/881)) —
  `download_folder` paginates children.
- SharePoint paging falls back to `$skip` with no next link
  ([#915](https://github.com/vgrem/office365-rest-python-client/issues/915)); custom
  headers are preserved across pages.
- Apostrophes in file paths ([#884](https://github.com/vgrem/office365-rest-python-client/issues/884)),
  in-memory upload streams ([#793](https://github.com/vgrem/office365-rest-python-client/issues/793)),
  and sharing-token UTF-8/padding ([#875](https://github.com/vgrem/office365-rest-python-client/issues/875)).
- `@odata.type` casting for directory collections
  ([#921](https://github.com/vgrem/office365-rest-python-client/issues/921)); principal
  path precedence ([#895](https://github.com/vgrem/office365-rest-python-client/issues/895));
  delta-token/custom query-param handling
  ([#948](https://github.com/vgrem/office365-rest-python-client/issues/948)); malformed
  JSON surfaced as `ClientRequestException`.

### Internal
- Generator metadata readers/model moved from `office365/runtime/odata` to
  `generator/odata`; generator checkpoints are no longer tracked.
- Unit suite consolidated into themed modules; pyright clean.

## [3.0.0]

### Breaking
- **Model properties are PEP 8 names** — 628 properties across SharePoint, Graph, and security moved from camelCase to snake_case (`file.serverRelativeUrl` → `file.server_relative_url`). The OData wire keys are unchanged, so `properties["ServerRelativeUrl"]`, `get_property()`, `ensure_property()`, and `$select`/`$expand` keep working. No aliases shipped: the old names raise `AttributeError`. Migration guide: [Upgrading from 2.x](docs/upgrading.md)
- **Python 2 dropped** — minimum Python version is now 3.8
- **ACS/SAML retirement** — `with_user_credentials` now raises `RuntimeError` for SharePoint Online. Use `with_username_and_password` (MSAL ROPC) instead. ACS App-Only (`with_client_credentials`) marked as deprecated.
- **USGovernment GCC endpoints corrected** — were using wrong URLs
- Model surface updated across SharePoint, Graph, and security namespaces (see Removed below)

### Added
- Full type hints across all modules (runtime, directory, onedrive, outlook, teams, sharepoint, intune, and more)
- `with_username_and_password` (MSAL ROPC) for SharePoint Online auth
- Substantially expanded Graph model coverage: Defender/security evidence types, subject rights requests, retention labels, threat intelligence, and more
- Expanded Intune (Cloud PC) and Teams admin/communication model surface
- New query/example modules for SharePoint, Graph, and Entra ID scenarios

### Changed
- Modernized SharePoint models and generator with Python 3 type hints (`Self`, `X | None`)
- `datetime.utcnow()` replaced with timezone-aware alternatives (Python 3.12+ deprecation)
- Generator tooling: `entity_type_name` support, EnumType generation, template-driven model props
- Credential/guard improvements for Entra ID multi-resource (via `ResourceName`)

### Fixed
- Cryptography CVEs updated to 48.0.0
- Circular import in `client_runtime_context.py` / `read_entity.py`
- `NameError: name 'List' is not defined` in `fields/collection.py`
- `single()` and `first()` return types (never return `None`)
- `AttributeError: 'str' object has no attribute 'get'` when SharePoint returns a string error payload
- Pyright type-checking errors across the library and tests

### Removed
- Python 2.7 support
- `.travis.yml` (use GitHub Actions instead)
- `requirements.txt` / `requirements-dev.txt` (use `uv`/`pyproject.toml`)
- Deprecated/renamed model classes superseded by the regenerated schema

### Internal
- CI moved to GitHub Actions (ruff, pyright, offline pytest)
- Dependency management via `uv` and `pyproject.toml`

---

## [2.6.2]

- Support Access Token Refresh for MSAL-provided tokens ([#953](https://github.com/vgrem/office365-rest-python-client/issues/953))
- Resolved `get_comments()` method issue ([#956](https://github.com/vgrem/office365-rest-python-client/issues/956))
- Added Reply-To and HTML ItemBody type support in `send_mail` ([#958](https://github.com/vgrem/office365-rest-python-client/issues/958))
- Fixed `File.open_binary` issue ([#960](https://github.com/vgrem/office365-rest-python-client/issues/960))
- Fixed linting GitHub Action ([#961](https://github.com/vgrem/office365-rest-python-client/issues/961))

## [2.6.0]

- Support for Azure environments in `ClientContext` (USGovernment, GCC High, etc.)
- Auto-renewal of authentication cookies for `with_user_credentials` (after 30 min expiry) ([#950](https://github.com/vgrem/office365-rest-python-client/issues/950))
- Support for worksheet [used range](https://learn.microsoft.com/en-us/graph/api/worksheet-usedrange) API ([#926](https://github.com/vgrem/office365-rest-python-client/issues/926))

## [2.5.14]

- Added `include_resource_data` to `SubscriptionCollection.add` ([#900](https://github.com/vgrem/office365-rest-python-client/issues/900), [#901](https://github.com/vgrem/office365-rest-python-client/issues/901))
- Added urllib percent-encoding to URLs ([#918](https://github.com/vgrem/office365-rest-python-client/issues/918))
- Microsoft Search API enhancements

## [2.5.13]

- JSON batch request fixes ([#835](https://github.com/vgrem/office365-rest-python-client/issues/835))

## [2.5.12]

- Batch request fixes and improvements ([#788](https://github.com/vgrem/office365-rest-python-client/issues/788))

## [2.5.11]

- Fixed error creating a choice field ([#873](https://github.com/vgrem/office365-rest-python-client/issues/873))
- Fixed `shares.by_url` method ([#872](https://github.com/vgrem/office365-rest-python-client/issues/872))
- Fixed failing driveItem move operation ([#627](https://github.com/vgrem/office365-rest-python-client/issues/627))
- Bumped MSAL dependency ([#869](https://github.com/vgrem/office365-rest-python-client/issues/869))

## [2.5.10]

- Fixed path issue when addressing drive items ([#866](https://github.com/vgrem/office365-rest-python-client/issues/866))

## [2.5.9]

- `DriveItem.get_files` and `get_folders` now retrieve all items beyond default page size ([#844](https://github.com/vgrem/office365-rest-python-client/issues/844))
- Fixed `__str__` raising exception when `DecodeUrl` is `None` ([#850](https://github.com/vgrem/office365-rest-python-client/issues/850))
- Added note for Entra ID permissions when updating SP metadata fields ([#847](https://github.com/vgrem/office365-rest-python-client/issues/847))

## [2.5.8]

- SharePoint resource addressing enhancements
- Introduced methods for granting and revoking delegated & application permissions

## [2.5.7]

- Added passphrase support in `ClientContext.with_client_certificate` ([#836](https://github.com/vgrem/office365-rest-python-client/issues/836))

## [2.5.6]

- Support for folder coloring in SharePoint API ([#693](https://github.com/vgrem/office365-rest-python-client/issues/693))

## [2.5.5]

- Better Range support in OneDrive API ([#745](https://github.com/vgrem/office365-rest-python-client/issues/745))

## [2.5.4]

- SharePoint authentication support for GCC High environments ([#794](https://github.com/vgrem/office365-rest-python-client/issues/794))
- Fixed listing folders instead of files ([#802](https://github.com/vgrem/office365-rest-python-client/issues/802))
- Fixed addressing shared drive items ([#801](https://github.com/vgrem/office365-rest-python-client/issues/801))

## [2.5.3]

- Added `file_name` parameter to `File.copyto` and `File.copyto_using_path` ([#787](https://github.com/vgrem/office365-rest-python-client/issues/787))
- Fixed import error for `TypedDict` on Python 3.7 ([#781](https://github.com/vgrem/office365-rest-python-client/issues/781))
- Fixed `parent_folder` / `parent_collection` empty when retrieving file by server-relative URL ([#764](https://github.com/vgrem/office365-rest-python-client/issues/764))
- Fixed 401 on site property update ([#735](https://github.com/vgrem/office365-rest-python-client/issues/735))
- Fixed recipient instance reuse ([#791](https://github.com/vgrem/office365-rest-python-client/issues/791))

## [2.5.2]

- Fixed missing `typing_extensions` dependency on older Python ([#762](https://github.com/vgrem/office365-rest-python-client/issues/762))
- File/folder addressing methods fixes ([#764](https://github.com/vgrem/office365-rest-python-client/issues/764))
- Fixed share file with password ([#766](https://github.com/vgrem/office365-rest-python-client/issues/766))
- Fixed change token entity type name ([#767](https://github.com/vgrem/office365-rest-python-client/issues/767))
- Documentation fixes ([#768](https://github.com/vgrem/office365-rest-python-client/issues/768))
- CI/Linting improvements ([#765](https://github.com/vgrem/office365-rest-python-client/issues/765))

## [2.5.1]

- Added conditional import of `ParamSpec` from `typing_extensions` ([#757](https://github.com/vgrem/office365-rest-python-client/issues/757))

## [2.5.0]

- Introduced `GraphClient.with_client_secret` and `GraphClient.with_username_and_password`
- Fixed `Folder.copy_to_using_path` ([#740](https://github.com/vgrem/office365-rest-python-client/issues/740))
- Fixed `File.download_session` ([#748](https://github.com/vgrem/office365-rest-python-client/issues/748))
- Fixed `ResourcePath` collection ([#744](https://github.com/vgrem/office365-rest-python-client/issues/744))
- Typing improvements (mypy/pyright support) ([#746](https://github.com/vgrem/office365-rest-python-client/issues/746), [#747](https://github.com/vgrem/office365-rest-python-client/issues/747))

## [2.4.4]

- Fixed `FieldCollection.add_dependent_lookup_field` ([#723](https://github.com/vgrem/office365-rest-python-client/issues/723))
- Fixed 404 error with `Web.get_file_by_server_relative_path` ([#722](https://github.com/vgrem/office365-rest-python-client/issues/722))

## [2.4.3]

- Support for interactive auth via `ClientContext.with_interactive`
- Support for OAuth2 device code auth ([#713](https://github.com/vgrem/office365-rest-python-client/issues/713))
- Fixed bug with losing event handlers ([#682](https://github.com/vgrem/office365-rest-python-client/issues/682))

## [2.4.2]

- Fixed error when file is addressed by path ([#645](https://github.com/vgrem/office365-rest-python-client/issues/645))
- File/folder addressing now supports site-relative and web-relative URLs
- Support for long-running actions in Teams API with polling status
