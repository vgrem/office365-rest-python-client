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
o365 <product> <noun> <action> [flags]        # what routing.route() already resolves
```
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
