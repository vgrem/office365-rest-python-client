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

The fix is ``token_cache=self._token_cache`` in two constructor calls,
``office365/runtime/auth/entra/authentication_context.py``. Nothing else is needed to persist a
session: MSAL refreshes from the cache, so a store that keeps the cache keeps the login.

## 2. Addressing — the honest measurement

A verb is reachable; an *instance* is not. ``Message.send`` needs a ``Message``, and the path to
one is a chain of navigation properties from a root. Measured over the tree, walking declared
navigations from ``GraphClient`` and ``ClientContext`` (reading the item type out of a generic
alias such as ``EntityCollection[Mailbox]`` — the same read ``item_type()`` does):

| | nouns |
| --- | --- |
| addressable from a root with no arguments | **851** |
| addressable with one ``{id}`` flag | 60 |
| addressable with nothing the model states | **1 029** |

Most of the gap is not an oversight in the model; those types are addressed by a *server path*
rather than by a navigation: ``Mailbox`` is ``/admin/exchange/mailboxes/{id}``, sharepoint
collections are ``web.lists.get_by_title(...)``, and 684 of the 1 029 are sharepoint nouns whose
addressing is per-list. ``office365/<p>/internal/paths/`` is where the unusual ones are spelled.

Two consequences, both worth deciding before any more code:

* the CLI can ship over the 911 nouns the model addresses and be *honest* about the rest
  (``o365 outlook message list`` works; ``o365 admin mailbox list`` needs a path first);
* covering the rest needs a **path template per noun**, and the only source that has one is the
  service metadata (``graphopenapi.yaml``, 35 MB, already in ``generator/metadata``). That is a
  generated *addressing* table, not a hand-written command table — the thing rejected earlier
  was a table of *words*, which the type system already states.

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
Argument flags are the method's own parameters, converted with the existing
``converters.parser_for(py_type)`` — 2 287 of 3 252 request-issuing methods are fully annotated
(152 annotate nothing, 11 take ``**kwargs``), so ``--help`` can be exhaustive without a
catch-all.

**S4 — The session file.** ``~/.o365/sessions.json``, mode ``0600``, ``O365_HOME`` overrides;
one object per audience: ``mode``, ``client_id``, ``tenant``, ``scopes``, ``environment``,
``version``, ``account``, and the MSAL cache dump. Secrets are **not** written (the cache
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
| 0 | ``token_cache`` in the two public flows + a test that a cache survives construction | 2 lines | persistence is possible at all |
| 1 | ``office365/cli`` = 4 functions: ``session()`` (file), ``login()`` (reads ``verbs_of(root)`` where ``name == "login"``, picks ``mode``, applies, verifies from claims), ``whoami()``, ``client()`` (rebuilds the root from a session) | ~120 lines | the session reads the declarations, and declares nothing |
| 2 | ``o365 outlook message list|get|send`` | ~40 lines + ``chain(root, noun)`` (~25) reading ``TypeSchema.navigations`` and ``item_type()`` | the engine is thin: one equality test against the library's own path builder |
| 3 | ``-o json|table|tsv``, ``--select``, ``--filter``, ``--top``, ``--all`` | output only | the data verbs already exist (``get_all``, ``QueryOptions``) |
| 4 | ``--yes`` gate from ``VerbMeta.confirm`` | small | the CLI can refuse before building a request |
| 5 | ``--help`` from signatures + docstrings | small | flags are exhaustive |

Start-up cost is the budget, not the code: 6 941 modules for the full index (~2 s), one product
0.2 s (``outlook``) to 1.2 s (``sharepoint``). A ``login`` must import only the auth modules, so
step 1 may not import ``routing``; step 2 pays the product import and nothing else.

## 5. Open, needs a decision

1. **Client id.** ``az`` works because Azure CLI ships its own app registration. This library has
   none, and every ``login`` mode requires ``--client-id``. Either we ship a public client id
   (an app registration allowing device-code/public client flows, consented per tenant) or
   ``--client-id``/``O365_CLIENT_ID`` stays mandatory. Not a coding question.
2. **Addressing scope.** Ship over the 911 addressable nouns now, or generate path templates from
   ``graphopenapi.yaml`` first to reach 1 940? The second is a generator job, not a CLI job.
3. **``[cli]`` extra** — dropped as S6 argues.
4. Nothing here adds a model declaration: no new decorator, no noun table, no client-id table.
