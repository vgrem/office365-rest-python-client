# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [3.3.1] - 2026-11-07

Two changes shape this line. Model types now declare what they read: every getter names
the OData member behind it, and a type's schema derives its projections from those
declarations instead of a hand-kept list. The migration layer becomes a set of portable
trees — mail, calendars, contacts and a bundle — so an export can be inspected, resumed
and imported into another tenant.

### Breaking

- The Teams export archive is the model's own JSON: `team.json` is `team.to_json()` with
  `members`, `installedApps` and `channels` attached, and `messages.ndjson` lines are
  `message.to_json()` plus `channel_id`. `TeamRecord`, `ChannelRecord`, `MemberRecord`,
  `TabRecord` and `AppRecord` are removed, with the extractor behind them;
  `TeamsExportOptions` moved to `migration.teams.adapters`.
- Every mailbox sidecar is the model's own JSON — `Message.to_json()`, `Event.to_json()`,
  `Contact.to_json()` — plus three provenance keys a model cannot know. A tree written by
  a pre-release build is refused by name (`refuse_legacy_sidecar`) instead of importing as
  empty fields.
- SharePoint getters declare the OData names they read (4,013 declarations, back-filled
  from the CSDL): `TypeSchema.of(Web).columns` goes 39 → 118 names and `.navigations`
  2 → 50, `List` 21 → 98, `File` 11 → 37, `Field` 3 → 41. A projection built from the old
  lists asked for navigation properties, which `$select` drops silently. Request bodies
  are unchanged: a declaration says what a *response* may carry, never what a request must.
- Graph getters declare them too: 6,911 declarations in 1,057 modules. `User` goes 21 → 81
  columns, `Group` 13 → 53, `DriveItem` 10 → 32, `Team` 9 → 17, `Channel` 5 → 13. 175
  members that were declared as columns are now declared as navigations, so `$select` no
  longer asks for them. Request bodies are unchanged.
- The back-fill that wrote those declarations is retired, not kept beside the tree it no
  longer changes. What guards them is a test that reads each declaration against the getter
  it sits above.
- A write payload no longer carries a value the service assigns: 117 SharePoint columns are
  declared `readonly` from a live write-and-read-back probe — all 37 of `File`, 43 more on
  `ListItem`, 13 on `Folder`, 17 on `Field`, 6 on `ContentType`. `to_json(profile)` drops
  them, so a request no longer echoes a server-owned value back.
- A column the service refuses is declared by the getter that reads it:
  `@odata(..., selectable=False)` replaces `ClientObject._unselectable`, and
  `ShieldAddRoleAssignmentPushdown` moved to `ListItem`, the one subclass a `$select`
  serves it for.
- A folder's content type order is the collection the CSDL declares, not one id:
  `Folder.content_type_order` and `unique_content_type_order` answer a
  `ClientValueCollection[ContentTypeId]`, so a caller reads `StringValue` off each member.
- An enum-typed Graph column returns the member, not the wire string: 386 type imports in
  241 modules moved out of the getter's body into the module block, where `declared_type`
  can see them — 403 columns. Compare by `.name`. A value no member names is kept as the
  service sent it, and one that differs only in case is that member.
- A `ClientValue` subclass no longer takes `@dataclass`: the base class applies
  `dataclass(cls, repr=False)` in `__init_subclass__`, once per class. A second pass over
  fields the first already consumed is a different class. Drop the decorator.
- A complex-typed Graph column declares its type as well: 745 more columns, 1,760
  value-typed in total, so the record importer no longer skips them as unknown.
- The names a dead `if TYPE_CHECKING:` block bound are reachable: 145 more columns answer a
  type — `ListItem.created` is `datetime`, not `None`. Four cyclic value types still cannot.
- `SP.User` loses the 58 profile getters that were a second copy of `SP.Directory.User`,
  plus `User.get_user_profile_properties` and `Web.site_id`. The profile fields live on
  `sharepoint.directory.users.user.User` or behind `PeopleManager`.
- `NavNode` and `WebNavigation` are removed: a captured navigation is the model's own tree,
  read through `Web.navigation.get_tree(recursive=True)`.
- `MigrationItem` no longer carries `author_id`/`editor_id` — they are
  `item.author.user_id` / `item.editor.user_id`, and the old keywords raise `TypeError`.
  `ItemReport` keeps both columns.
- `PagePayload` is gone (a page item is a `SitePage`); `PAGE_LIBRARY_TEMPLATE`,
  `SITE_PAGE_CONTENT_TYPE_PREFIX` and `is_modern_page` left `migration.sharepoint.pages` in
  favour of `is_page_library(list)`; `offline_context()` moved to
  `office365.migration.offline`.
- `IcsProfile` is `IcsDialect`, and each family's record is one class with methods:
  `CalendarEventRecord` and its helpers are `EventRecord`, the `contact_*` helpers are
  `ContactRecord`, and `STANDALONE_EVENT_TYPES`/`event_kind` are gone.
- The permission machinery moved to `office365.permissions`, which exports
  `require_permission`, `declared`, `PermissionRequirement`, `Requirement`,
  `Requirement.join`, `ResourceName` and `index`. The `office365.directory.permissions`
  modules that held it are gone, and `declared(method, flow=...)` raises instead of
  answering an empty requirement when the method names nothing under that flow. The
  package keeps Graph's permission entities, which are model types, not vocabulary.
- A declaration and a requirement name the **API resource** its permissions belong to:
  `@require_permission(resource=ResourceName.SharePoint, delegated=[...])`. A name is only
  a grant on the API that defines it, so names from two resources are never merged
  (`Requirement.join` refuses). The default is `ResourceName.Graph`.
- `office365.sharepoint.workflow.task` is gone with the second `SPWorkflowTask` it
  declared; import `SP.Workflow.SPWorkflowTask` from
  `office365.sharepoint.workflow.sp_workflow_task`.
- `ListItem.moderation_status`, `SitePage.moderation_status` and
  `UserInfoItem.o_data___moderation_status` answer an `SPModerationStatusType` member
  instead of the raw integer, so a comparison against a literal reads false.
  `SitePage.moderation_status` is `readonly` as well.
- The metadata doors on the model types are gone; the type's schema answers instead:
  `select_all()` is `TypeSchema.of(...).columns`, `expand_all()` is `.expansions`,
  `select_facet(f)` is `.columns_of_facet(f)` and `odata_name(a)` is `.name_of(a)` — on a
  `ClientValue` too.

### Added

**Model metadata**

- A value declares itself the way an object already did: `ClientValue.__init_subclass__`
  runs `dataclass(cls, repr=False)` and reads the schema from those fields, with
  `@dataclass_transform()` telling a type checker what the decorator said.
- A type's schema carries its identity and its roots beside its properties: `_schema.key`
  and `_schema.versions`, from `@key(...)` and `@version(...)`.
- `@key("tenantId")` declares which property spells a *type's* identity: what re-anchors an
  entity's path when the value is set, and what a read forces into `$select`.
- One index answers for both carriers, and the class states it once, in
  `__init_subclass__`: `TypeSchema.of(Model)` is an attribute read, with nothing scanned
  twice.
- A schema derives its projections from that index on the first ask: `columns`,
  `navigations`, `expansions`, `readonly`, `persistable`, `system`, `beta_names`,
  `canonical_names`, `beta_only`, `stable_only` and `facets`.
- A field can declare what the service treats as the same value:
  `@odata(name="birthday", compare=Compare(format="date"))`, where `Compare` carries
  `casefold` and `fallback`.
- `@odata(navigation=True)` marks an `$expand`-only member and `@odata(expandable=False)`
  one `$expand` will not follow alone: `TypeSchema.of(Event).expansions` no longer names
  `extensions`, which the service refuses without a `$filter`.
- `@odata(system=True)` records provenance: the metadata declares no such name, the service
  spells it on the item payload.
- `hydrate(payload, profile=None)` is the one in-place read verb on `ClientObject`,
  `ClientValue` and `ClientResult`, answers `self` so it chains, and reads what `to_json()`
  writes when no profile is given.
- `JsonProfile.scoped(Model, only=..., without=...)` narrows any profile to some properties of
  one model, and `entity.to_json(COMPARABLE)` spells a model in the comparable form
  (`office365.runtime.odata.comparable`), so two copies that differ only by what the service
  rewrites compare equal and a real difference does not.
- One serialization contract lives in `office365.runtime.serialization`
  (`JsonSerializable.to_json(profile=None)`, `PropertyReceiver.set_property(...)`), and
  `JsonProfile` keeps only what it uses.
- `values_of(cell)` answers the items of a collection cell in every shape a read or a
  payload produces.
- `ListItem.value_column(name)` and `string_value_column(name)` spell the item columns a
  Lookup or Person value travels under: `<name>Id`, and the read-only `<name>StringId`.
- Every `$select` column of a served package resolves a declared type, including the twelve
  value-object getters that carried no annotation.

**SharePoint items**

- `ListItem.set_system_metadata(values, new_document_update=False)` writes the system fields
  of a list item in one `ValidateUpdateListItem` request: a `datetime` as `...Z` UTC, a
  `User` as its login.
- `ListItem.restore_fidelity(created, modified, author, editor, approval, ...)` writes what a
  copy of an item cannot carry in its payload — the dates, the authorship, the approval
  columns — in one request.
- `SPModerationStatusType` spells the approval column's five values, and the three getters
  that read the column answer it.

**Outlook mail**

- `MessageCollection.add_from_mime(data)` creates a draft from RFC 822 bytes — an `.eml`
  file as it sits on disk — posting them base64-encoded as `text/plain`.

**Migration**

- `migration_client(client)` applies the background-workload policy in one call: a shared
  `RateLimiter` on the context's transport, plus `x-ms-throttle-priority: low` on a Graph
  client.
- `IdentityMap` maps source principals onto target principals for authorship and ACLs, from
  a CSV (`source,target[,system_id]`), an e-mail domain rewrite or a policy.
- Mail as a portable tree: `MailFolderSource` and `MailExportTarget` write one `.eml` plus
  one sidecar per message and a `manifest.jsonl` index; `EmlTreeSource` and `MailboxTarget`
  import it back through `add_from_mime`. A resumed run skips what is on disk, and mail is
  verified by `mime_digest` — the semantic headers plus a hash per decoded part — because
  Exchange re-serialises every message it stores. Each family has its options class
  (`MailExportOptions`, `MailImportOptions` and a matching pair per family).
- Calendars and contacts round-trip the same way: `CalendarSource`/`IcsExportTarget` and
  `ContactSource`/`VcfExportTarget` write one `.ics` (RFC 5545 folding, `TZID`, `RRULE`,
  `VALARM`) or one `.vcf` plus a sidecar per record, and `IcsTreeSource`/`CalendarTarget`
  and `VcfTreeSource`/`ContactTarget` import them, replaying Graph's own `recurrence`
  object from the sidecar.
- `MigrationItem.metadata` carries adapter-defined envelope attributes — a message's
  subject, recipients, categories — into the manifest, so a portable export writes its own
  index. The runner never interprets it.
- `MigrationJob.plan()` states the fidelity forecast before it enumerates
  (`plan.fidelity`, `MigrationJob.fidelity()`, `export_reports`), and `describe_fidelity`
  reports a product's own dimensions.
- A target accepts a captured structure (`sp_list=` / `structure=`) and replays it before
  the first write, so a bundle can be imported into a library that has none of its shape.
- The server-side package target grants SharePoint **groups** as well as users
  (`PermissionEntry.principal_type="group"`, `owner`, `owner_groups`), because a `<Group>`
  without an `Owner` fails the whole ingestion job.
- `FileVersion.sort_key` compares version labels as numbers (`"1.9"` before `"1.10"`), and
  `BasePermissions.value` / `from_value(mask)` own the 64-bit permission mask both ways.
- A page's fields are spelled by the library (`publishing/pages/fields.py`: `PAGE_FIELDS`,
  `BODY_FIELDS`), and `SPBuiltInContentTypeId.SitePage` is the content type base a modern
  page derives from.
- A declared value is held under the attribute its declaration names: `UserIdInfo` holds
  `name_id`, and `ClientValue.set_property` / `get_property` resolve a wire spelling through
  the schema, the way `to_json` already did in the other direction.
- A schema's projections are held to what they claim by a walk over the whole package
  (`tests/unit/test_declaration_ratchets.py`): `$select` and `$expand` never offer the same
  name, `expansions` stays inside `navigations`, a facet offers only names `$select` can
  carry.

**Long-running operations**

- An operation is watchable, not just waitable: `stream()` / `astream()` yield each snapshot,
  terminal one last, and raise nothing for a failed outcome. `wait()` is the same loop with
  the failure policy applied.
- `OperationStatus` carries the timeline (`created_date_time`, `last_action_date_time`
  timezone-aware with a UTC fallback, `retry_after`), and a `partiallySucceeded` operation is
  terminal-but-neither-outcome.
- `RespondAsyncRequest.execute()` returns an operation either way: pollable when the service
  answered `202`, already terminal when it finished in the submitting round-trip
  (`LongRunningOperationResult.completed(...)`, `is_completed`).
- One engine behind every wait (`office365.runtime.operation.Operation`): deadline,
  `Retry-After` pacing, jitter, progress hook, cooperative cancel and `transient_statuses=`
  as data.
- `MigrationServerJob.job_wait()` returns the wait instead of running it, so polls can be
  streamed, cancelled or monitored concurrently.

**Service limits**

- Graph's throttling quotas are data: one `quotas` module per product (`outlook`, `teams`,
  `onedrive`, `onedrive.workbooks`, `reports`, `security`, `directory`, `communications`),
  each registering itself at import, plus `GLOBAL_QUOTAS`. Two more modules carry the limits
  a migration meets at scale: `subscriptions/quotas.py` and `onenote/quotas.py`.
- A model references a row instead of re-spelling it (`CALL_RECORD_QUOTAS`, `EXCEL_QUOTAS`),
  and a quota is declared where the request is made — including on the operation that makes
  the call.
- `@limit` composes: a second decorator on one target adds its rows, and stacked
  declarations share one `Limits:` section. `declared_limits()` answers each row once, reads
  `@limit` off the MRO, and `limits_of(cls)` answers class-level rows too.
- 97 of the 122 published rows are reachable from some `_schema`; the 25 that are not are
  named rather than forgotten.

**Permissions**

- The migration layer names what it needs: the 54 public request-issuing operations under
  `office365.migration` declare their grant, the 37 SharePoint ones as a `@site_access` rung
  (`capture_*`/`read*` are `READ`, `apply_*`/`provision_*` are `WRITE`). No package is left
  to exempt: `migration` left `UNTRACKED`, so `index(office365).debt()` is `{}` for every
  package.
- `@derived_from(callee)` stamps a wrapper with the same `PermissionRequirement` the callee
  carries, read once at import, so a pass-through cannot drift from the method it drives.
  The request detector now counts `execute_query_async` and `execute_batch_async`.
- `office365.permissions.TokenClaims` parses a JWT's payload and answers one requirement:
  the audience says which API issued it, `scp` names the delegated permissions, `roles` the
  application ones. The signature is not checked — the token came over TLS.
- Both authentication contexts expose `access_token`, acquiring it once if they hold none,
  so a caller can ask what a token proves before sending a request. A live test's skip
  decision reads that token first and the tenant's grants only where the token cannot speak.
- `office365.permissions.catalog(resource)` answers what an API publishes —
  `Catalog.publishes(name, kind)`, `requires_admin_consent(name, kind)` and the names
  themselves — generated from that API's own service principal.
- The convenience methods on `GraphClient` (`has_`/`grant_`/`get_`/`revoke_`, delegated and
  application) take `resource`, defaulting to Microsoft Graph.
- SharePoint's eight names are four rungs — `AllSites.Read` → `.Write` → `.Manage` →
  `.FullControl`, with `Sites.Read.All` → `.FullControl.All` beside them for app-only —
  declared on `Web` and `SecurableObject` (20 methods), on the everyday objects (`File` 51,
  `ListItem` 35, `ListCollection` 5), on `Site` (70, of which 31 act outside the site
  collection) and on every remaining owner.
- Tenant administration declares what it needs: `Tenant` (284 operations),
  `SiteMoveService` (86) and `Office365Tenant` (43) name a rung and, where the permission
  alone does not decide, the SharePoint Administrator role — 413 declarations. The six page
  kinds, the workflow task, all 21 Teams operations, and every Communications, Directory,
  OneDrive, tenant-configuration, compliance, social and plumbing operation declare too.
- `office365.permissions` exports `DirectoryRole`, a `str` enum carrying Entra's own
  display name, and `@odata(identity=...)` lets a type say which members name the object, so
  a securable's ACL is read through the type rather than a spelled-out `$expand`.
- A blocker says which calls asked for it: the preflight report gives a requirement a `via`
  column. An IDE's test runner gets `OFFICE365_LIVE=1` in `.env` as its switch, and nothing
  writes `.env` any more — the wizard that merged its findings back into it is gone.

### Changed

- A created type says which of its columns it does not send: `List`, `Web` and the SharePoint
  principal types answer the question `ListItem`, `Folder`, `File`, `Field`, `ContentType`
  and `SitePage` already did.
- A list stops sending the columns the service will not keep: 41 of `List`'s 98 columns are
  declared read-only from a write-and-read-back probe, not from a reading of the docs.
- A site and a group do the same: `Web` gains 62 read-only declarations, `Group` 8.
- A caller asks for a role, not for a name: a member can declare `facet=AUTHORSHIP`,
  `facet=PERMISSIONS` or `facet=MODERATION`, and `TypeSchema.columns_of_facet(...)` answers
  the columns of that role.
- A declaration carries no fact nobody reads: `filterable`, `sortable`, `searchable`,
  `nullable` and `description` are gone from `ODataPropertyMeta` and `@odata(...)`; not one
  of the 4,883 declarations set any of them.
- An export is a projection of the type, not of the response: every writer that goes through
  `records.iter_records` derives its columns from the model, so an item carrying an extra
  field no longer reorders every header.
- A list item's own columns are declared on the item: `AuthorId`, `EditorId`, `Created`,
  `Modified`, `FileRef` and `FileLeafRef` are `system=True`, and `is_file` / `is_folder` read
  `file_system_object_type` rather than the presence of something else.
- A navigation node answers the flags the service sends: `is_visible` and `is_external` read
  `IsVisible`/`IsExternal`, so every node no longer answers `None`.
- A securable declares the ACL flag it has always read: `has_unique_role_assignments` is
  `readonly`, and `FirstUniqueAncestorSecurableObject` and `RoleAssignments` are navigations.
- `Field` answers what a column holds — `is_taxonomy`, `is_lookup`, `is_person`,
  `is_multi_valued`, `is_multi_choice`, `is_value_object` — over `schema_property(...)` and
  `is_taxonomy_column(...)`, so a reader need not parse the schema.
- The runtime owns the spelling facts the migrator had duplicated: `iso_z` and
  `wall_clock_text` for the two date spellings a SharePoint write takes, `normalize_guid`
  over `uuid.UUID`, and `checksum(data)`.
- The calendar's spelling, document and record are three modules (`calendar_profile`,
  `calendar_codec`, `calendar_models`), so an enum that gains a member is a table row.
- The bundled transports bound the read and write phases as well as connect (`(10 s connect,
  300 s read)`, with write and pool bounds on httpx), so a server that stops responding
  mid-response fails as a transient error instead of blocking the caller.
- `MigrationJob.plan()` fails fast on a fidelity flag the adapter pair cannot honour, one
  phase before the first write.
- `LongRunningOperationResult.monitor_url` is `str | None`; the ingestion-job monitor counts
  its deadline on the clock; `PollableOperation.wait(sleep=None)` can be woken by `cancel()`.
- A published row answers the type that spends it: `BaseItem` and `Permission` declare
  `FILES_QUOTAS`, so `limits_of(DriveItem)` no longer returns nothing while
  `office365/onedrive/quotas.py` publishes nine rows for it.
- The lockfile and the dev tooling need Python 3.11, not 3.10: every patched release of
  `filelock` and `tornado` declares `requires-python >=3.11`, so a 3.10 lock branch could
  only keep a vulnerable pin. The package itself still installs on 3.8.

### Fixed

- `order_by` never reached the service. `QueryOptions` emitted its Python attribute names as
  query keys, so a sorted read asked for `$order_by` — which Graph answers `200` to and
  ignores. Every standard option is now spelled as the specification spells it
  (`order_by` → `$orderby`), and a `custom` key is still the caller's own.
- A small file was never attached to a message that already exists.
  `Message.upload_attachment` sends anything under 3 MB inline, and that path only
  registered a child on the message's `attachments` collection — a child that rides the
  message create.
- A multi-value column could be created but not updated. A bare array is refused on both
  writes (`InvalidClientQueryException`), so `{"results": [...]}` is the column's shape.
- A `$select` read narrowed every later read of the object it was made on:
  `ReadEntityQuery` appended its properties to the object's own `query_options`.
- A team site was returned before it existed, and at a url the alias does not spell:
  `{base}/teams/{alias}` was a guess, and this tenant served the site at `/sites/TeamSite…`.
- A page's web parts were requested without the cast that names the type. `SitePage.web_parts`
  asked for `pages/{id}/webParts` and the service answered `Resource not found for the
  segment 'webParts'`; it asks for `pages/{id}/microsoft.graph.sitePage/webParts` now.
- A permission name the API does not publish was counted as a grant: a directory records
  whatever string a grant names, so a token can carry a name Microsoft Graph never minted.
  `Requirement` now asks the committed catalogue.

**Model**

- Four `ClientValue` fields defaulted to a value *instance* (`trigger: WorkflowExecutionTrigger
  = WorkflowExecutionTrigger()`), so every value ever constructed aliased it; they use
  `field(default_factory=...)`.
- The term store refused every type cast the payload carried: `/termStore` is served by
  SharePoint's own model and answers `The specified type named microsoft.graph… is not
  recognized`, with or without the leading `#`.
- A flags combination is a value the enum cannot spell, and the collection dropped it: Graph
  returns `"password,softwareOath"`, which no member names, so reading a strength policy
  raised `TypeError`. The collection keeps the wire spelling.
- A Teams schedule entity sent the service's timestamps back: `ChangeTrackedEntity` declares
  `createdDateTime` and `lastModifiedDateTime` `readonly`, as the CSDL marks them computed.
- Three upload sessions sent a range the service refuses: Graph requires a positive multiple
  of 320 KiB, and the defaults were `1000000`, `1000000 * 3` and 4 MiB.
- Activating a directory role was refused for the type name in its own payload:
  `DirectoryRole` inherited the base `entity_type_name` and announced itself as
  `#microsoft.graph.DirectoryObject`.
- `DirectoryRoleCollection.assign` failed with no subject: a name with no template left the
  lookup `None` and raised `AssertionError` from inside a response listener. It raises
  `ValueError` naming the role.
- `Team.messaging_settings` read the guest settings, because the getter spelled
  `guestSettings` in its body.
- `SignIn.location` read the status: the city, state and country came back empty because the
  getter spelled `status`, the name a neighbouring getter already owned.
- `FileStorageContainer.entity_type_name` named no namespace: it answered
  `graph.fileStorageContainer` where every other type name starts with `microsoft.graph.`.
- A team listed from the group collection answered a string for `visibility`: `GET
  /groups/{id}` sends `Public` where `GET /teams/{id}` sends `public`.
- An enum column kept the wire string: the generator writes a getter's type as a
  function-local import plus a `TYPE_CHECKING` entry, both invisible to
  `typing.get_type_hints`, so the declaration resolved to `None`.
- A `timedelta` column held the ISO string: sixteen columns declare `timedelta` and
  `_SCALAR_CONVERTERS` had no entry, so a read gave `'PT30M'`.
- A cyclic type's declaration was lost: `ChatInfo` and `ConditionalAccessGrantControls`
  cannot be imported at module level, so the getter imports them for itself and
  `get_type_hints` saw a `NameError`.
- A column whose getter stated no type was a column the runtime could not read: the last
  120 were hand-written getters whose only mention of a type was the fallback they passed to
  `properties.get`.
- `SharingInformation.domain_restriction_settings` read the anonymous-link expiry, the name
  its neighbour already owned.

**Runtime**

- `to_json()` is 62% faster on a payload of built-in scalars: `serialize_value` answers a
  `str`, `int`, `bool`, `float` or `None` before asking whether the value is an object.
- `parse_datetime` tries ISO parsing first — 15.6× faster — and still reads a `.NET` stamp
  with seven fractional digits on every supported interpreter.
- A path is 17.8% cheaper to build: `ODataPathBuilder` skips a special-character replacement
  the value does not contain.
- Snapshot emission is 7.7% cheaper: `Progress` is built positionally on the hot path.
- The two retention feeds reject every query option they are offered, so a bare `GET` is
  what they get.
- The library imports on Python 3.11 again: `TypeSchema` gave five `Mapping` fields a
  `default_factory` a type checker reads as one shared instance.
- A throttled request waits the interval the service asked for: `execute_query_retry`
  retried on its own backoff and ignored `Retry-After`.
- `to_json()` no longer emits `__`-prefixed bookkeeping (`__etag`, `__deferred`,
  `__odata_type`): they describe the response, not the entity.
- `DateTimeTimeZone.parse()` reads what callers pass: a Graph `dict`, an aware `datetime`, a
  string. A `dict` used to raise `AttributeError`, so `EventCollection.add(start={...})` was
  unusable.
- `str()` on a scalar collection renders the list (`[freeBusyRead, read]`) instead of the
  internal type name, and `repr()` is quoted and type-qualified.
- A limit prints what it measures: `200 requests / 24h` rather than `/ 86,400s`.

**SharePoint (client)**

- `List.export()` exports files: the loop compared the wire's number against
  `FileSystemObjectType.File` and `0 == File` is `False`.
- A query bound to a subweb addresses the subweb: `ClientQuery.url` pasted the query's own
  path onto the service root.
- `FeatureCollection.add(verify_if_activated=True)` activates a feature the collection does
  not list: the guard asked `GetById('<guid>')`, which answers `null` at site scope.
- `Utility.resolve_principal_in_current_context` accepts its flags as enums: `scopes` and
  `sources` are `Edm.Int32` bit flags and the call sent the enum's repr.
- A `SitePage` projection is one the service accepts: `TemplateScope` answers `400
  NotSupported`, so the getter declares `selectable=False`.
- A page's canvas is one property, not two: a read-only twin shadowed the writable
  `canvas_content`, so `TypeSchema.name_of("canvas_content")` raised.
- A copy job addresses its objects by absolute URL and reports progress only for a real job:
  `create_copy_jobs` wrapped `exportObjectUris` in a `{"results": [...]}` envelope the
  service rejects.
- Two endpoints that cannot work over REST say so: `PeopleManager.get_user_profile_properties`
  is the reader for `UserProfilePropertiesForUser`, and `Tenant.get_site_subscription_id`
  raises `System.NotSupportedException`.
- A page payload no longer carries an emptied nested value: `SitePageFieldsData(Title="x")`
  serialises as `{"Title": "x"}`, not `{"Title": "x", "CoAuthState": {}}`, so a farm that
  never had that property does not refuse the create.

**Migration (client-side)**

- The list target and the library target carried the same three hooks over one form payload:
  one built the `Created`/`Modified` dict, another merged the approval dict at two points,
  and the library kept its own UTC→local converter with a per-value cache. Both resolve
  authors and approval into a pending record and hand it to `ListItem.restore_fidelity`
  once, with `web_local_dates=True` on the library side.
- The SharePoint assessment reads a list item's columns through the item (`item.file_ref`,
  `is_file`, `has_unique_role_assignments`) instead of the JSON bag.
- The list migration classifies a column once, through the column: five per-run caches over
  one `fields` read became `_source_fields()` and the column's own predicates.
- A file's current version no longer appears twice in its history: `File.Versions` includes
  the current version, which the read passed through as an older one.
- A plain list is no longer routed to the server-side package: `Manifest.xml` has no `<List>`
  object, so a list record became a `<File>` whose content was the record's `dict` repr.
- A replayed view is created with the columns the target list has, and a column it drops is
  reported rather than failing the whole replay.
- A re-run of `configure()` writes nothing, and whatever a structure replay cannot reproduce
  is reported on `target.warnings`.

**Migration (server-side package path)**

- A resumed package run re-attaches to the job it already submitted: the job id lived only in
  memory, so `commit()` submitted a second ingestion job for the same package.

**Migration (Outlook)**

- Calendar and contact exports derive their projection from the model
  (`TypeSchema.of(Event).columns`, `TypeSchema.of(Contact).columns`).
- `iCalUId` is read as the service spells it: the envelope asked for `iCalUid`, so every
  sidecar carried `"ical_uid": null` and the `.ics` `UID` fell back to the Graph id.
- A recurring event's sidecar carries JSON, not `repr` text: `recurrence` is flattened
  through `to_json()` instead of reaching `json.dumps` as a typed value.
- Verification compares in the source's timezone: Exchange renders times in the signed-in
  mailbox's zone, so an event copied into a differently-zoned mailbox reported a mismatch
  while the instants were identical.

**Permissions**

- Three live suites were skipped for a licence the tenant already had: they declared retail
  E5 SKU part numbers, and the test user's seat is `DEVELOPERPACK_E5`.
- The preflight report dropped a whole flow instead of resolving it: `--verify` could build a
  client only for the password and secret flows.
- `ServicePrincipal.get_application_permissions` reported a subset of the client's grants: it
  read `appRoleAssignedTo`, which Graph answers truncated even when expanded.
- `ServicePrincipal.grant_application_permissions` granted twice, because its idempotency
  check read the same truncated collection.
- `ServicePrincipal.get_delegated_permissions` answered from one grant: a resource holding a
  tenant-wide grant plus per-user ones reported only the first.
- `ServicePrincipal.revoke_delegated_permissions` removes the scope from grants on this
  resource only, not from every grant of the client app that spells the name.
- Ten application permissions were declared that Microsoft Graph does not publish: the eight
  workbook methods that open, refresh and close an Excel session and the two `/search/query`
  methods named `Files.ReadWrite`.
- A live suite named a permission Microsoft Graph does not publish, and `--grant` died on it:
  `tests/directory/test_governance.py` listed `Approve.AppConsentRequests.Read.All` beside
  `EntitlementManagement.Read.All` as an any-of.

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
