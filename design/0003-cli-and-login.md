# 0003 — A command line: session first, then addressing

A plan, not a record. Everything marked *measured* was read off this tree with a probe, not
assumed; the probe is described so the number can be re-taken.

The library already answers "which method runs ``outlook message send``" (``office365/routing.py``,
7 969 commands over 1 940 nouns). Two things are missing before a command line can run anything:
a session it does not have to re-authenticate for, and a way to *address* the noun it named.
This note fixes the first, measures the second, and proposes the order of work.

## 1. What the model already states about authentication — measured

| Fact | Where it is declared |
| --- | --- |
| 5 client roots | ``GraphClient``, ``ClientContext`` (sharepoint), ``ExchangeAdminClient`` (exchange), ``TaxonomyService``, ``ExcelService`` |
| 12 login verbs | ``@verb(role="action", effect="local", name="login", mode=…)`` on the two public roots |
| Graph modes | ``client-secret``, ``certificate``, ``interactive``, ``username-and-password``, ``device-flow`` |
| SharePoint modes | ``client-secret``, ``certificate``, ``interactive``, ``device-flow``, ``username-and-password``, ``ntlm``, ``app-only`` |
| 6 clouds | ``office365/azure_env.py`` — ``AzureEnvironment`` + ``EnvironmentEndpoints`` (graph, login) |
| session fields | ``GraphClient.__init__(tenant, scopes, token_cache, environment, authority, version)`` |

So the *shapes* of login are declared. ``VerbMeta.mode`` is what distinguishes the five ways —
the word ``login`` is one word, six ways to do it. A command line reads that: ``--mode``.

**The root of a product is readable, not declared anew.** Five ``ClientRuntimeContext``
subclasses exist; the root for product *p* is the one whose module lives under
``office365.<p>``, else ``GraphClient``. ``sharepoint`` → ``ClientContext``,
``exchange`` → ``ExchangeAdminClient``, the 27 Graph products → ``GraphClient``.

### 1.1 The gap that blocks a CLI today — measured

``GraphClient(token_cache=SerializableTokenCache())`` is honoured by the **confidential** client
flows only. The two flows a command line can use build their MSAL app without it:

```
device flow:   token_cache passed to PublicClientApplication -> False
interactive:   token_cache passed to PublicClientApplication -> False
```

(Probe: replace ``msal.PublicClientApplication`` with a stub that records its kwargs, call
``AuthenticationContext(...).with_device_flow("id")``.) ``with_device_flow`` even has a
"reuse the signed-in account" branch — which can only ever find the account it created in the
same process. In a CLI, every process is a new process: the login would be lost on exit.

It took two fixes, not one, because the cache was dropped at two levels. The flows built
their MSAL app without it; and above them ``GraphClient.pending_request()`` built its
``GraphRequest`` without it, so ``GraphClient(token_cache=...)`` was stored on the client and
read by nobody. The same read found a second silent drop beside it: ``GraphClient(scopes=...)``
never reached the context either, which used ``https://graph.microsoft.com/.default``
regardless.

Fixed at both levels — ``token_cache=self._token_cache`` in the three public-flow constructions,
and ``scopes``/``token_cache`` passed from ``GraphClient`` to ``GraphRequest`` to
``AuthenticationContext``. Nothing else is needed to persist a session: MSAL refreshes from the
cache, so a store that keeps the cache keeps the login. ``ExchangeAdminClient`` already threaded
its cache; ``ClientContext`` authenticates through a different provider
(``office365/runtime/auth/authentication_context.py``) that has no cache to thread.

So the store keeps **two** things, and the second is what makes sharepoint work: the MSAL cache
where the root has one, and the access token itself in every case. Re-opening a session reads the
token the login kept; nothing re-runs the mode, and nothing needs a secret. Both providers answer
the same read — ``pending_request().authentication_context.access_token``, "acquired on first
read, cached, never validated" — which is what a login states once and what a replay attaches
through ``with_access_token``. A sharepoint token is not refreshed (that provider has no cache),
so it is kept until it expires and renewed by logging in again; a graph token refreshes from the
cache beside it. Measured: ``o365 sharepoint login --mode certificate`` then ``o365 sharepoint web
get`` prints the web, and ``o365 login --mode client-secret`` then ``o365 directory user get``
prints the user.

**A command does not log in — measured, and this is why.** The first live run reached
``username-and-password``, and the second command failed: ``with_username_and_password() missing
2 required positional arguments``. Replaying the mode needs the password, and a session must not
keep one. So a command reads the access token the session already holds
(``pending_request().with_access_token(...)``) and says ``run login again`` when it has expired.
One rule for all six modes, no secret on disk, and nothing to thread through MSAL a second time.

## 2. Addressing — the honest measurement

A verb is reachable; an *instance* is not. ``Message.send`` needs a ``Message``, and the path to
one is a chain of links from a root. A link, in this model, is **a property that says what it
returns**: ``GraphClient.me`` answers ``User``, ``User.messages`` answers ``MessageCollection``,
and ``EntityCollection[Note]`` is read through its origin because that is what a generic holds at
run time. Nothing is guessed and no URL is composed — the walk is ``chain(root, target)`` in
``office365/routing.py``, and each step is ``getattr``.

Two limits keep it honest: a getter that *needs an argument* is not a link (the walk has nothing
to pass it), and a link that is only declared as a navigation without a getter is not a link
either (``getattr`` would fail).

| | measured |
| --- | --- |
| types reachable from the two roots | **315** (234 graph, 81 sharepoint) |
| nouns addressable in the eight largest products | **169 of 1 520** |
| the same, allowing one hop into a feed's item type | 200 |

Per product, noun-and-feed pairs the walk reaches: ``directory`` 51/380, ``sharepoint`` 61/684,
``onedrive`` 20/104, ``outlook`` 10/30, ``teams`` 10/69, ``intune`` 10/233, ``planner`` 5/12,
``todo`` 2/8. Re-take any row with ``chain()`` itself: for every ``nouns(product)`` entry, ask
``chain(GraphClient(), entry.collection or entry.entity)``.

**Retracted: 851 / 60 / 1 029 and "911 of 1 940".** Those numbers came from an earlier probe
that is not reproducible by an attribute walk, and an attempt to re-derive them with declared
navigations *and* annotated getters gives 221, not 911. The table above is what the code does;
the earlier figures are not used anywhere.

The gap is not an oversight in the model. Most of the rest are addressed by a *server path*
rather than by a link: ``Mailbox`` is ``/admin/exchange/mailboxes/{id}``, sharepoint collections
are ``web.lists.get_by_title(...)``, and 684 of the unaddressable nouns are sharepoint ones whose
addressing is per-list. What the model does **not** state, anywhere, is *how to address one item
of a feed*: ``todo task`` is reachable only as ``me.todo.lists[?].tasks``, and no declaration says
what that ``?`` is for a given collection. ``ClientObjectCollection`` has ``single(expression)``,
``first``, and ``get_by_alternate_key``, but no per-type statement of the key an item is
addressed by — ``get_by_id`` exists on 12 collections and is not a rule.

### 2.1 What a command runs now — measured

``o365 <product> <noun> <action> [flags]`` resolves the route, walks the links, and calls the
method the verb names. Flags are the method's own signature (the machinery ``login`` already
uses); the object it is called on is the one the walk reached.

* ``o365 outlook message list`` → ``https://graph.microsoft.com/v1.0/me/messages``, records on
  stdout. The URL is the one the library's own builder makes, produced code-based and offline
  with a stand-in MSAL and a scripted transport, and again live against a real tenant.
* ``o365 directory user get`` → ``GET /me``, live.
* ``o365 outlook message`` with no action → the 16 actions the noun answers, read off
  ``verbs_of`` for the entity and its feed (``list``, ``get``, ``create``, ``send`` …).
* ``o365 outlook attachment get`` → exit 2, and a line that says the noun is declared but nothing
  walks there: no URL is invented for it.

Reaching a noun by an ``{id}`` is therefore the next *model* question, not the next CLI question.

### 2.2 The path is the user's; the walk is only a guess

The grammar is ``<product> <noun> [navigation ...] [action]``. The words after the noun are the
getters the line wants walked, so ``o365 sharepoint web lists list`` is ``web.lists.get()`` — a
getter per word, checked against the model, with no URL composed and no second table:

* a word is an **action** when the type it lands on answers one (``Route.commands``);
* otherwise it must be a **getter** the type holds (``routing._links``), and it is walked;
* if the words end without an action, the actions of the type they reached are printed.

This matters because two routes to one type are two different URLs, and only the caller knows
which was meant. Measured on the noun ``list``: ``chain`` answers ``('web',
'access_requests_list')`` — a real feed of the wrong list — because breadth-first finds the first
getter declared to return a ``ListCollection``, and ``Web.access_requests_list`` is one. Spelling
``web lists`` gives ``https://<site>/_api/Web/lists``. So a route is still walked when the line
does not say how, but the walk is a **guess**, ``--help`` prints which one it will take
(``Walk web -> lists, then get() on ListCollection``), and the spelled path is the answer to it.

A word that resolves to neither is refused with both inventories, or with the closest names:
``o365: sharepoint web foder holds no 'foder'; did you mean folders, root_folder?`` and
``o365: sharepoint web lis holds no 'lis'; did you mean list, lists?`` — an action and a getter in
one suggestion, which is exactly the ambiguity a user has.

The cost, measured cold: 1.29 s for ``sharepoint web lists`` (the index dominates), 1.31 s adding
a word, 0.23 s for ``outlook message attachments``.

## 3. Decisions proposed

**S1 — One store, keyed by audience.** A session belongs to an *audience* (``graph``,
``sharepoint``, ``exchange``), not to a product: ``outlook``, ``teams``, ``intune`` and 24 others
answer to one Graph token. The audience is read from the package the answering type lives in —
measured over the five largest products (1 267 nouns): 583 answer with a
``office365.entity.Entity``, 674 with a ``office365.sharepoint.entity.Entity``, 10 with neither,
and exactly two nouns answer with the other audience's base (``sharepoint tokenresponse`` is a
Graph type). No new declaration: it is the same package fact ``service_of`` already reads.

**S2 — Login is not product-scoped.** ``o365 login`` logs into Graph; ``o365 sharepoint login``
into SharePoint; ``o365 exchange login`` into Exchange. The two-slot form is the root's empty
noun, which is why ``sharepoint login --tenant … --client-id … --client-secret …`` already reads
correctly: ``login`` is a verb of ``ClientContext``, not of a noun inside it.

**S3 — Grammar.**
```
o365 login|logout|whoami|sessions [--audience graph|sharepoint|exchange] [flags]
o365 <product> <noun> [navigation ...] [action] [flags]   # what routing.route() resolves
```
The words between the noun and the action are getters the model states, so the command line
names its own URL and the model only checks it (§2.2). An action ends the line; a word after one
is refused rather than read as a further step.
An audience word is only read when a session verb follows it, because ``sharepoint`` is both an
audience and a product: ``o365 sharepoint login`` is the session, ``o365 sharepoint web get`` is
the product. ``graph`` is an audience and no product at all, so its nouns are addressed by product
(``o365 directory user get``), and ``o365 graph`` alone prints the usage.
Argument flags are the method's own parameters, converted with the existing
``converters.parser_for(py_type)`` — 2 287 of 3 252 request-issuing methods are fully annotated
(152 annotate nothing, 11 take ``**kwargs``), so ``--help`` can be exhaustive without a
catch-all.

**S4 — The session file.** ``~/.o365/sessions.json``, mode ``0600``, ``O365_HOME`` overrides;
one object per audience: ``mode``, ``client_id``, ``tenant``, ``scopes``, ``environment``,
``version``, ``account``, the access token it kept, and the MSAL cache dump where the root has one. Secrets are **not** written (the cache
refreshes); ``--store-secret`` opts in and says so. No new dependency: ``json`` + ``os.chmod``,
not ``platformdirs``.

**S5 — ``whoami`` costs no request.** The access token is a JWT; decoding its claims gives
``upn``/``appid``, ``tid``, ``scp`` or ``roles`` — the difference between a delegated and an
app-only session, and the fastest way to see a failed grant. No verification of the signature,
which is right for display.

**S6 — Drop the ``[cli]`` extra.** Auth needs ``msal`` (already core), output needs ``json``/``csv``
(stdlib), parsing needs ``argparse`` (stdlib). An extra with no dependencies would lie about what
installing it buys. ``[project.scripts] o365 = "office365.cli:main"`` is the whole packaging story.

**S7 — Destructive calls read ``VerbMeta.confirm``**, which is already declared and currently
empty by design (93 of 158 writes are irreversible in fact but cannot be proved so from the
model). Until that ledger is filled the CLI asks ``--yes`` for every ``effect=write`` action it
cannot justify — refusing with a reason beats guessing.

## 4. Order of work

| # | Step | Size | Proves |
| --- | --- | --- | --- |
| 0 | ``token_cache`` in the three public flows + a test that it reaches MSAL | 3 lines | persistence is possible at all — **done** |
| 1 | ``office365/cli.py``: ``login`` (reads ``verbs_of(root)`` where ``name == "login"``, picks by ``--mode``, derives every flag from the two signatures), ``whoami``, ``logout``, and the store | 270 lines | the session reads the declarations, and declares nothing — **done** |
| 2 | ``o365 <product> <noun> <action>``: ``chain(root, target)`` (25 lines) plus the command path in ``cli.py`` (110 lines) | 163 lines net | the engine is thin: the URL comes out of the model, and the flags out of the signature — **done**, live |
| 3 | ``-o json|table|tsv``, ``--select``, ``--filter``, ``--top``, ``--all`` | output only | the data verbs already exist (``get_all``, ``QueryOptions``) |
| 4 | ``--yes`` gate from ``VerbMeta.confirm`` | small | the CLI can refuse before building a request |
| 5 | ``--help`` from signatures + docstrings | small | flags are exhaustive |

Start-up cost is the budget, not the code. Measured after step 1: ``o365 whoami`` imports
**99 modules in 0.03 s** and never touches ``routing`` or ``sharepoint``; ``login --help`` pays
for the root it describes — 2 281 modules / 0.64 s for ``graph``, 1 054 / 0.31 s for
``sharepoint``. Step 2 pays the product import and nothing else; the full noun index (6 941
modules, ~2 s) is only needed to list what exists, which no command does.

## 5. Open, needs a decision

1. ~~**Client id.**~~ Decided: ``--client-id`` (or ``O365_CLIENT_ID``) is mandatory, and a login
   without it is refused with that reason. Shipping a public client id is a product question,
   not a coding one, and can be answered later without changing the grammar.
2. **One item of a feed.** 169 of 1 520 nouns are reachable by walking; the rest need either an
   ``{id}`` in the path or a server path template. The first is a model question (nothing states
   what addresses one element of a collection), the second a generator question
   (``graphopenapi.yaml``). Neither belongs in the CLI: ``o365 outlook attachment get`` refuses
   rather than composing a URL.
3. **``[cli]`` extra** — dropped as S6 argues.
4. Nothing here adds a model declaration: no new decorator, no noun table, no client-id table.

## 6. The name a class declares — the marker that is missing

A command needs three facts from the model, and it now reads all three from metadata: the noun
(``ClientObjectCollection.item_type()``), the action (``@verb``), and the product
(``__product__`` in the package). A fourth it still has to guess — **which family a type belongs
to** — and today it guesses by walking the MRO for one of the two ``Entity`` bases. That guess is
wrong for three models:

| model | imports | should be |
| --- | --- | --- |
| ``office365.copilot.admin.CopilotAdmin`` | ``office365.sharepoint.entity.Entity`` | ``office365.entity.Entity`` |
| ``office365.copilot.root.CopilotRoot`` | ``office365.sharepoint.entity.Entity`` | ``office365.entity.Entity`` |
| ``office365.directory.authentication.methods.sms_target.SmsAuthenticationMethodTarget`` | ``office365.sharepoint.entity.Entity`` | ``office365.entity.Entity`` |

All three are Graph types (``copilot/admin``, ``copilot/root``, ``sms-authentication-method-target``),
so today each answers ``SP.<name>`` as its wire name, ``Id`` as its key, and the v3 entity path.
Measured before the fix: ``o365 copilot admin get`` asked for the **sharepoint** session. The
product rule (``TypeSchema.product``) answers ``graph`` for them now, so only the wire, the key
and the path are still wrong, and the fix is one import line each.

Eleven more SharePoint types inherit neither base — ``term``, ``term-set``, ``term-store``,
``term-group``, ``taxonomy-item``, ``client-side-page``, ``spo-operation``,
``site-collection-management-service``, ``picker-entity-information``, ``group-site-manager``,
``token-response`` — and the honest consequence is already the behaviour: ``chain`` answers
``None`` for all eleven, so no command claims them.

**The real finding is bigger, and it is the opposite of a gap.** The OData name is not missing:
it is stated **4 642 times** as an instance property —

```python
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.User"
```

— 3 722 model classes and 910 enums. ``ClientObject.entity_type_name`` **already** reads
``self._odata_type_name`` first, and ``ClientValue.entity_type_name`` is nothing but
``return self._odata_type_name``. The class fact exists; what does not exist is anybody
*declaring* it. Measured consequences:

- ``edm_type_name(cls)`` answers ``None`` for ``Web``, ``User``, ``Term``, ``CopilotRoot`` and
  ``ClientSidePage``, so resolution falls through to constructing a throwaway instance.
- ``addresses_version(cls)`` is ``False`` for every model, because ``getattr(cls,
  "entity_type_name")`` is a ``property`` object, not a string. ``ClientQuery._require_declared_member``
  returns early on that, which means **the beta/stable gate never runs for an operation name** —
  its own docstring says it is the difference between a local error and a 404 naming a segment.

One line per class states the same fact where a class can be asked for it:

```python
    _odata_type_name: ClassVar[str] = "microsoft.graph.User"
```

That is **10 189 lines fewer** in generated code (4 642 × 2 saved, 4 642 added), it makes
``edm_type_name`` a dictionary read instead of an instantiation, it turns the operation gate on,
and it lets ``_audience`` be ``TypeSchema.product`` for every type without an MRO walk. Enums have
to keep the property: a class attribute in an ``Enum`` body becomes a **member** (measured), and
the sunder spelling is refused (``ValueError: _sunder_ names … are reserved``).

**Prototyped on one file, and the swap alone is not enough.** Removing ``User.entity_type_name``
and declaring ``_odata_type_name = "microsoft.graph.User"`` was enough for ``edm_type_name(User)``
(None -> ``microsoft.graph.User``, no instantiation, no import needed in the file), but
``User(None).entity_type_name`` then answered **``microsoft.graph.DirectoryObject``**: both
``Entity`` bases derive a name, cache it in ``self._entity_type_name``, and never look at the fact,
so a class that inherits from another would start lying about itself.

So three readers come first, and each is smaller than what it replaces:

- ``ClientObject.entity_type_name`` becomes the one reader of all three sources, in the order the
  object knows them: ``_entity_type_name`` (stated about *this* object - a list item's real type
  arrives from the server, ``listitem.py:1094``), then ``_odata_type_name`` (declared by the
  class), then a derived default.
- ``office365/entity.py`` and ``office365/sharepoint/entity.py`` stop overriding the property and
  override only the default (``microsoft.graph.<camel>`` / ``SP.<Name>``): 10 and 6 lines become
  2 each.
- ``addresses_version`` reads ``edm_type_name(model)`` instead of ``getattr(model,
  "entity_type_name")``, which is the difference between the operation gate running and not.

Then the sweep is mechanical (``ast`` in, ``ast`` out, 4 632 files, −3 lines each), and it changes
what a *class* answers, so it lands with the generator template change
(``generator/build/member.py`` emits the property; ``generator/tools/type_identity.py`` reads the
shape) and a live run, not just ``--offline``.

## 7. Completion — possible, and what it costs

The grammar is already a tree: products (22, 0.16 s to enumerate), nouns (``nouns(product)``),
navigation words *or* actions at every level after the noun (``_links`` for one, ``Route.commands``
for the other — the same two maps the run reads), flags (a method signature). Completion is a
fourth reader of those, never a fourth source, and it is one hidden verb plus a six-line shell
function that ``o365 completion bash|zsh`` prints.

Following a spoken path costs nothing extra: the partial line is resolved by ``route(product,
*complete_words)`` — the same function that runs it — and the candidates are
``sorted({*_links(here), *commands})``. Measured: 50 candidates at ``sharepoint web <TAB>`` in
0.98 s (``list``, ``list_templates``, ``lists`` all offered for ``lis``), and one at ``web lists
<TAB>``. The single ordering judgement is that an action is offered before a getter of the same
name, because ``list`` is both.

Cost is the whole question, measured per level, cold:

| level | what it reads | time |
| --- | --- | --- |
| product | the 22 packages | 0.16 s |
| noun | ``nouns('outlook')`` | 0.22 s |
| noun | ``nouns('teams')`` | 0.42 s |
| noun | ``nouns('directory')`` | 0.97 s |
| noun | ``nouns('sharepoint')`` (684) | 1.34 s |
| action | ``route(product, noun)`` — reuses the same index | +0.10 s |

Two answers, and the decision is a product one:

1. **No cache.** Tab on ``o365 sharepoint `` takes 1.3 s. Correct, never stale, and paid only
   by the two large products.
2. **A cache of a declaration.** The index is a function of the library version, so it is written
   once per version under ``~/.o365/nouns/<version>/<product>.json`` and read thereafter (~10 ms).
   A stale cache can only *offer* a noun that no longer routes, and the run refuses it — the cache
   is never the answer to "what exists", only a faster copy of one.

Nothing about completion is a table: no name in it is authored.
