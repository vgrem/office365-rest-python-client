"""A command line that reads the declarations instead of restating them.

Grammar, ``az``-shaped and with the audience first because a token belongs to one::

    o365 login [--audience graph|sharepoint|exchange] [--mode device-flow] [--tenant <tenant>] \\
               [--client-id <id>] [--scopes User.Read Mail.Read]
    o365 whoami [--audience ...]
    o365 logout [--audience ...]
    o365 <product> <noun> [navigation ...] [action] [-o table|wide|json|csv|tsv|url|name] [flags]
    o365 sharepoint use <site> [--as <name>]  -- address this session at one site collection
    o365 sharepoint context [ls|use <name>|inspect] -- where it is addressed, and what it remembers
    o365 help <any words>               -- the page for them, or ``-h`` at the leaf
    o365 completion bash|zsh|fish        -- print the shell script that completes the words
    o365 completion --warm [product ...] -- fill the cache, so no TAB pays an import

There is no flag table here. ``--tenant`` reaches ``GraphClient.__init__`` because the
constructor declares ``tenant``; the same flag reaches ``ClientContext.with_device_flow``
because *that* declares it - one rule, read off the signatures:

    a flag named by the constructor sets the session, every other flag is passed to the
    login method the ``--mode`` selects.

So the six ways to log in stay one word with a ``--mode``, because ``@verb`` already
states the difference, and the credentials are whatever the method says they are.

Two things the command line supplies rather than accepts: the ``token_cache`` (the session
file *is* the cache, and it is read back on every login, so a refresh token it already holds
is renewed rather than asked for again) and the site, which a login can find rather than be told.

What it has to be *told*, it asks once and keeps in ``~/.o365/config.json`` -- your file, read
and never written here: ``client_id``, ``tenant``, ``site``. In that order a flag wins, then
``O365_CLIENT_ID``/``O365_TENANT``/``O365_SITE``, then the file, then an error that names it.
This library ships no app registration of its own, so a client id has to come from somewhere;
the difference worth having is being asked once instead of every run. A ``--password`` is a flag
like any other, which also means it is visible in the process list; a secret store behind
``--authority``/``--client-secret`` is the better habit.

A SharePoint session is addressed at one *site collection*, because that is the boundary the
model draws: ``ClientContext(base_url)`` is one site, ``client.tenant`` is the tenant that holds
them, and ``clone(url)`` switches site while reusing the token and the transport. So the store
keeps the sites a session has been pointed at and which one is current, ``o365 sharepoint use``
changes it, ``context`` lists them the way ``docker context ls`` does, ``--site``/``O365_SITE``
overrides it for one command, and every sentence that could cost something -- the ``--yes``
refusal, ``--dry-run``'s URL -- names the site it would reach. A login with no site asks
Graph's ``/sites/root`` through a session that already holds a token, else takes Microsoft's
documented ``https://<label>.sharepoint.com`` for a ``<label>.onmicrosoft.com`` tenant, and
otherwise refuses rather than writes a guess into the store.

A session is one token, so it is kept per audience and not per product. What is kept is
the access token itself, plus MSAL's cache where the root has one to hold: ``GraphClient``
and ``ExchangeAdminClient`` do, and ``ClientContext`` authenticates through a different
provider that does not, so a sharepoint session is kept until its token expires and is then
renewed by logging in again.

A read prints a table, not the payload: the columns the *type* says a read of it asks for --
the members stamped ``@odata(default=<rank>)``, read as ``TypeSchema.defaults`` -- which is the
answer a command line was asked for. ``-o json`` prints everything the object loaded, and
``--columns`` says which names the table shows. ``Web`` is 118 fields loaded and two printed;
the other 116 are not hidden, they are unasked for. A type that ranks nothing prints its
payload, because a settings object with sixteen config switches has no name a reader came for.
Which column is a link is a declaration too (``@odata(facet=link)``, ``TypeSchema.links``), and
the drawing lives in ``office365/runtime/render.py`` -- a header row, numbers right-aligned, a
cut value marked with ``…``, a sentence when nothing was found -- because the notebook ``repr``
in ``display.py`` answers a different question.

The words a shell may offer are the model's own, so they are read from it rather than listed
here: ``o365 __complete`` is the hidden half of the protocol (absent from ``--help`` for the
reason ``kubectl __complete`` is: it is not a command a person types) and it imports no package
until a noun is already on the line. ``o365 completion bash|zsh|fish`` prints the script that
calls it, and ``--warm`` fills the cache once, at login, so that no TAB pays an import.
"""

from __future__ import annotations

import argparse
import base64
import functools
import importlib.util
import inspect
import json
import os
import sys
import textwrap
import time
import types
from collections.abc import Mapping
from enum import Enum
from pathlib import Path
from typing import Any, Union, get_args, get_origin
from urllib.parse import urlparse

#: An audience is one token, not one product: ``outlook``, ``teams``, ``intune`` and 24
#: more all answer to ``graph``. The module is named because two of the three packages do
#: not re-export their root class.
AUDIENCES = {
    "graph": "office365.graph_client",
    "sharepoint": "office365.sharepoint.client_context",
    "exchange": "office365.exchange",
}

#: The mode a login picks when none is given, if the root declares it.
DEFAULT_MODE = "device-flow"

#: Parameters the command line fills itself, so they are never flags.
SUPPLIED = ("self", "token_cache", "token_callback")

#: The words an audience prefixes: ``o365 sharepoint login`` is a session, not a noun.
SESSION = ("login", "whoami", "logout")

#: The audiences whose root is addressed at one site: a ``ClientContext`` is one site
#: collection, so it is also the one place a session can be *switched*. A graph or exchange
#: root is addressed by the token alone.
CONTEXT_AUDIENCES = ("sharepoint",)

#: How many sites a session remembers. Enough to switch by name, few enough to print.
SITE_MEMORY = 10

#: The two words that move a session's site boundary, for the audiences that have one.
SITE_WORDS = ("use", "context")

#: What a licence report prints as: the record formats, and none of the address ones - ``url`` and
#: ``name`` answer for a noun's records, and a plan is not something a client can address.
LICENCE_FORMATS = ("table", "wide", "csv", "tsv", "json")

#: The formats whose stdout is the data alone: the sentence describing the report goes to stderr,
#: so `o365 licences -o csv` pipes into a spreadsheet without a stray line at the top.
PIPED_FORMATS = ("csv", "tsv", "json")

#: The derived index the generator writes: the model's discovery answers as data (built by
#: ``generator graph --index``, never edited). Reading it costs 4 ms; computing the same answers
#: by importing the tree costs 5.2 s, which is what the levels below cannot afford.
INDEX = Path(__file__).with_name("index.json")


def main(argv: "list[str] | None" = None) -> int:
    """Run one command, returning the process exit code."""
    words = list(sys.argv[1:] if argv is None else argv)
    # The completion protocol is answered before the grammar is read: a shell asks with the
    # words already typed, which are not a command, and asks a hundred times an hour.
    if words[:1] == ["__complete"]:
        return _complete(words[1:])
    if words[:1] == ["completion"]:
        return _completion(words[1:])
    # `licences` is the one word that asks the tenant a question about the whole library rather
    # than about one product, so it is answered before a product is looked for.
    if words[:1] == ["licences"]:
        return licences(words[1:])
    return _dispatch(*_audience_words(words))


def _dispatch(audience: str, words: "list[str]") -> int:
    """Read the grammar: a page to show, a session to open, or a route ending in an action."""
    if not words or words[0] in ("-h", "--help", "help"):
        # `help` is the same question `-h` asks, by name: it names the route it wants a page
        # for, and answers the served list or the usage when it names nothing.
        if words[1:]:
            return _help(audience, words[1:])
        print(_served(audience) if audience else _usage())
        return 0 if audience else 2
    word, rest = words[0], words[1:]
    if word in SESSION or (audience in CONTEXT_AUDIENCES and word in SITE_WORDS):
        return _session(audience, word, rest)
    # `o365 graph <noun>` names no product: the audience word was standing in for one, because
    # 25 products share the graph token and none of them is a package called `graph`.
    product = audience if audience and not _is_product(word) else word
    if product != word:
        # The audience word was the product's stand-in, and only `graph` needs one: 25 products
        # share its token and none of them is a package called `graph`, so it has to be named.
        print(f"o365: {product} is a token, not a product; {_served(product)}", file=sys.stderr)
        return 2
    if not rest:
        print(f"o365: unknown command {product!r}\n{_usage()}", file=sys.stderr)
        return 2
    noun, rest = rest[0], rest[1:]
    # The words name the route and stop where the first flag starts; a flag's value is not a word.
    cut = next((position for position, item in enumerate(rest) if item.startswith("-")), len(rest))
    return command(product, [noun, *rest[:cut]], rest[cut:])


def login(audience: str, argv: "list[str]") -> int:
    """Authenticate, then keep the session in the store."""
    from office365.runtime.verbs import verbs_of

    root = _root(audience)
    logins = {attribute: meta for attribute, meta in verbs_of(root).items() if meta.name == "login" and meta.expose}
    modes = sorted({meta.mode for meta in logins.values()})
    parser = argparse.ArgumentParser(
        prog=f"o365 {audience} login",
        description=f"Log in to {audience}. Every flag is a parameter {root.__name__} declares.",
    )
    parser.add_argument("--mode", choices=modes, default=DEFAULT_MODE)
    seen = {"mode"}
    _flags(parser, root, seen)
    for method in (getattr(root, attribute) for attribute in logins):
        _flags(parser, method, seen)
    args = parser.parse_args(argv)

    method = next(attribute for attribute, meta in logins.items() if meta.mode == args.mode)

    given = _accepted(args, root) | _accepted(args, getattr(root, method))
    # A client id and a tenant are facts about the person, not arguments that change between
    # runs, so they are looked for once: this run's flag, their environment, their config file.
    prefs = _prefs()
    wanted = set(_signature(root).parameters) | set(_signature(getattr(root, method)).parameters)
    given["client_id"] = given.get("client_id") or os.environ.get("O365_CLIENT_ID") or prefs.get("client_id", "")
    if not given["client_id"]:
        parser.error('no client id: pass --client-id, set O365_CLIENT_ID, or put "client_id" in ' + str(_config()))
    tenant = given.get("tenant") or os.environ.get("O365_TENANT") or prefs.get("tenant", "")
    if tenant and "tenant" in wanted:
        given["tenant"] = tenant
    if "base_url" in wanted and not given.get("base_url"):
        given["base_url"] = _site_for(given.get("tenant", ""), prefs)
        if not given["base_url"]:
            parser.error('no site: pass --base-url, set O365_SITE, or put "site" in ' + str(_config()))

    import msal

    # The session file *is* the cache, and it is read back: a cache that is only ever written
    # renews nothing, so every login would show a device code for a token MSAL could have
    # renewed from the refresh token the store already held.
    kept = _load().get(audience) or {}
    wants_cache = any("token_cache" in _signature(fn).parameters for fn in (root, getattr(root, method)))
    cache = None
    if wants_cache:
        cache = msal.SerializableTokenCache()
        if kept.get("cache"):
            cache.deserialize(kept["cache"])
        given["token_cache"] = cache

    constructor = {name: value for name, value in given.items() if name in _signature(root).parameters}
    client = root(**constructor)
    getattr(client, method)(**{name: value for name, value in given.items() if name not in constructor})
    # Both providers state the same property: acquired on first read, cached, never validated.
    token = client.pending_request().authentication_context.access_token or ""
    claims = _claims(token)

    sessions = _load()
    kept = _remember(sessions.get(audience) or {}, str(constructor.get("base_url") or ""), "")
    sessions[audience] = kept | {
        "mode": args.mode,
        "method": method,
        "client_id": given["client_id"],
        "constructor": {name: _plain(value) for name, value in constructor.items() if name != "token_cache"},
        "claims": claims,
        # The token itself, so an audience whose root has no cache to hold is still kept;
        # the cache beside it is what MSAL refreshes from when the root can.
        "token": {"access_token": token, "expires_on": int(claims.get("exp", 0))},
        "cache": cache.serialize() if cache is not None else "",
    }
    _save(sessions)
    print(_summary(audience, sessions[audience]))
    return 0


def whoami(audience: str) -> int:
    """Print what each kept session says about itself, without sending a request."""
    sessions = _load()
    if audience:
        sessions = {name: entry for name, entry in sessions.items() if name == audience}
    if not sessions:
        print(f"o365: no session for {audience or 'any audience'}; run o365 login", file=sys.stderr)
        return 1
    for name, entry in sorted(sessions.items()):
        print(_summary(name, entry))
    return 0


def logout(audience: str) -> int:
    """Forget one session, or every session."""
    sessions = _load()
    dropped = [name for name in ([audience] if audience else list(sessions)) if sessions.pop(name, None)]
    if not dropped:
        print("o365: nothing to log out of", file=sys.stderr)
        return 1
    _save(sessions)
    print("logged out: " + ", ".join(dropped))
    return 0


def _session(audience: str, word: str, rest: "list[str]") -> int:
    """Run one word that speaks to the session rather than to the service."""
    if word == "login":
        return login(audience or "graph", rest)
    if word == "whoami":
        return whoami(audience)
    if word == "logout":
        return logout(audience)
    if word == "use":
        return use(audience, rest)
    return context(audience, rest)


def use(audience: str, argv: "list[str]") -> int:
    """Address this session at one site collection, and remember it.

    The site is the boundary the model draws -- one ``ClientContext`` per site collection, one
    token for all of them -- so switching changes the address and nothing else: the kept token
    is reused, and ``clone`` shares the transport when a caller switches inside one process.
    The choice is checked with one read, the site's ``Title``, because a wrong URL should fail
    here rather than in front of a delete.
    """
    sessions = _load()
    entry = sessions.get(audience)
    if entry is None:
        return _refuse(f"no session for {audience}; run o365 {audience} login")
    parser = argparse.ArgumentParser(
        prog=f"o365 {audience} use",
        description="Address this session at one site. A URL, a remembered site, or a name under /sites/.",
    )
    parser.add_argument("site", help="the site: a URL, a remembered name, or a name under /sites/")
    parser.add_argument("--as", dest="name", default="", help="remember it under this name")
    parser.add_argument("--no-check", action="store_true", help="remember it without reading its title")
    args = parser.parse_args(argv)
    try:
        url = _address(audience, entry, args.site)
    except LookupError as err:
        return _refuse(str(err))
    title = ""
    if not args.no_check:
        try:
            site = _client(audience, site=url).web.get().select(["Title", "Url"]).execute_query()
        except Exception as err:  # the service's own answer, said as it came
            return _refuse(f"{_short(url)}: {err}")
        title = getattr(site, "title", None) or ""
    sessions[audience] = _remember(entry, url, title, args.name)
    _save(sessions)
    print(f"context: {_short(url)}" + (f" — {title}" if title else ""))
    return 0


def context(audience: str, argv: "list[str] | None" = None) -> int:
    """Where this session is addressed, and the sites it can be moved to: read, never asked.

    ``context`` answers both at once, ``context ls`` is the list with the current one marked,
    ``context use`` is :func:`use`, and ``context inspect`` is the current site on its own lines.
    A noun with those verbs is ``docker context``'s shape, because a site is what a docker
    context is: an endpoint a session is addressed at, whose name is what a person types.
    """
    entry = _load().get(audience)
    if entry is None:
        return _refuse(f"no session for {audience}; run o365 {audience} login")
    spoken = list(argv or [])
    if spoken[:1] == ["use"]:
        # Handed to `use` whole, so that its own flags (``--as``, ``--no-check``) reach it.
        return use(audience, spoken[1:])
    parser = argparse.ArgumentParser(
        prog=f"o365 {audience} context",
        description="The sites this session can be addressed at, and which one it is at.",
    )
    parser.add_argument("word", nargs="?", choices=("ls", "inspect"), default="")
    args = parser.parse_args(spoken)
    current = _current(audience, entry)
    if args.word == "inspect":
        print(_inspect(audience, entry, current))
        return 0
    if args.word == "ls":
        print(_sites(entry, current, audience))
        return 0
    print(_summary(audience, entry))
    others = [site for site in entry.get("contexts", []) if str(site.get("url", "")).rstrip("/") != current]
    if others:
        print("  also: " + ", ".join(_site_name(str(site.get("url", ""))) for site in others))
    else:
        print(f"  another site: o365 {audience} use <url>")
    return 0


def _sites(entry: "Mapping[str, Any]", current: str, audience: str) -> str:
    """The sites a session remembers, the current one marked: what ``docker context ls`` prints.

    The name is what a ``use`` accepts, so it is the first column; the URL follows because two
    sites of different tenants can share a name.
    """
    rows = [
        (str(site.get("url", "")).rstrip("/"), str(site.get("name") or ""), str(site.get("title") or ""))
        for site in entry.get("contexts", [])
        if site.get("url")
    ]
    if not rows and not current:
        return f"no sites remembered; o365 {audience} use <url>"
    if not rows:
        # A store written before sites were listed still knows where it is, so say that rather
        # than claim nothing is remembered.
        rows = [(current, _site_name(current), "")]
    named = [(url, name or _site_name(url), title) for url, name, title in rows]
    width = max(len(name) for _, name, _ in named)
    lines: "list[str]" = []
    for url, name, title in named:
        mark = "*" if url == current else " "
        lines.append(f"{mark} {name.ljust(width)}  {_short(url)}" + (f"  {title}" if title else ""))
    return "\n".join(lines)


def _inspect(audience: str, entry: "Mapping[str, Any]", current: str) -> str:
    """The current site, one fact per line: the address as it is sent, and the name it answers to."""
    if not current:
        return f"no site: o365 {audience} use <url>"
    held = next(
        (site for site in entry.get("contexts", []) if str(site.get("url", "")).rstrip("/") == current),
        {},
    )
    lines = [f"site:  {current}", f"name:  {held.get('name') or _site_name(current)}"]
    if held.get("title"):
        lines.append(f"title: {held.get('title')}")
    return "\n".join(lines)


def _current(audience: str, entry: "Mapping[str, Any]") -> str:
    """The site a session is addressed at: the one `use` set, else what login was given."""
    return str(entry.get("current") or (entry.get("constructor") or {}).get("base_url") or "").rstrip("/")


def _address(audience: str, entry: "Mapping[str, Any]", wanted: str) -> str:
    """A site URL from what was typed, without asking the service what sites exist.

    A remembered site answers by its title or its name, a full URL is taken as given, and a
    bare name means the site of that name under the host this session already knows -- because
    a person switching sites types ``finance``, not the tenant's hostname again.
    """
    for known in entry.get("contexts", []):
        url = str(known.get("url", "")).rstrip("/")
        if not url:
            continue
        # A site answers to the name it was given, the one its URL spells, and its title: the
        # three things a person can remember having typed or read.
        answers = {
            str(known.get("name") or "").lower(),
            _site_name(url).lower(),
            # The host as well as the URL, so the root site answers to ``use contoso.sharepoint.com``.
            url.split("://", 1)[-1].lower(),
            str(known.get("title", "")).lower(),
            url.lower(),
        }
        if wanted.lower() in answers:
            return url
    if "://" in wanted:
        return wanted.rstrip("/")
    host = urlparse(_current(audience, entry)).netloc
    if not host:
        raise LookupError(f"no site to resolve {wanted!r} against; pass a full URL")
    if "/" in wanted:
        return f"https://{host}/{wanted.strip('/')}"
    return f"https://{host}/sites/{wanted}"


def _remember(entry: "Mapping[str, Any]", url: str, title: str, name: str = "") -> "dict[str, Any]":
    """The session with ``url`` current, and first among the sites it remembers.

    The site that was current before is remembered too, even when a login wrote it and no
    ``use`` ever named it: the store's ``constructor.base_url`` is a site like any other, and
    losing it on the first switch would make the earlier answer unreachable.
    """
    url = url.rstrip("/")
    held = list(entry.get("contexts", []))
    previous = str(entry.get("current") or (entry.get("constructor") or {}).get("base_url") or "").rstrip("/")
    if previous and all(str(site.get("url", "")).rstrip("/") != previous for site in held):
        held.insert(0, {"url": previous, "title": ""})
    kept = [site for site in held if str(site.get("url", "")).rstrip("/") != url]
    was = next((site for site in held if str(site.get("url", "")).rstrip("/") == url), {})
    # A name is kept only when it was said: the URL's last segment already answers otherwise,
    # and writing it down would make a rename look like a different site.
    chosen = name or str(was.get("name") or "")
    here: "dict[str, Any]" = {"url": url, "title": title or str(was.get("title") or "")}
    if chosen:
        here["name"] = chosen
    return {**entry, "current": url, "contexts": [here, *kept][:SITE_MEMORY]}


def _site_name(url: str) -> str:
    """The name a site answers to by default: its last path segment, or ``root`` at the host."""
    rest = url.split("://", 1)[-1].rstrip("/")
    return rest.rsplit("/", 1)[-1] if "/" in rest else "root"


def _site_for(tenant: str, prefs: "Mapping[str, str]") -> str:
    """The site a login should address, when it was not told one.

    Three answers, most trustworthy first: the site in the config file; the tenant's own, read
    from Graph's ``/sites/root`` through a session that already holds a token; and Microsoft's
    documented default host for a ``<label>.onmicrosoft.com`` tenant. Nothing is derived from a
    vanity domain, because a domain name does not say where its SharePoint lives.
    """
    return os.environ.get("O365_SITE", "") or prefs.get("site", "") or _graph_site(tenant) or _derived_site(tenant)


def _graph_site(tenant: str) -> str:
    """``https://<host>`` for the tenant one stored Graph session already reads, else nothing.

    ``/sites/root`` is the documented way to ask a tenant where its SharePoint is, and it costs
    one request and no prompt because it reuses the token the store keeps. It is only trusted
    for the tenant that session belongs to, so a second tenant never inherits the first's host.
    """
    entry = _load().get("graph") or {}
    known = str((entry.get("constructor") or {}).get("tenant") or (entry.get("claims") or {}).get("tid") or "")
    if not known or (tenant and tenant.lower() != known.lower()):
        return ""
    try:
        root = _client("graph").sites.root.get().select(["webUrl"]).execute_query()
    except Exception:  # no live token, no Sites.Read.All, no answer: say nothing rather than guess
        return ""
    return str(getattr(root, "web_url", "") or "").rstrip("/")


def _derived_site(tenant: str) -> str:
    """Microsoft's default SharePoint host for ``<label>.onmicrosoft.com``, or nothing.

    A tenant's SharePoint domain starts out as its tenant name, so this is the documented
    default rather than a guess at one -- renameable afterwards, which is why whatever it
    answers is checked with one read before it becomes what the session is addressed at.
    """
    label = tenant.strip().lower()
    if not label.endswith(".onmicrosoft.com"):
        return ""
    label = label[: -len(".onmicrosoft.com")]
    return f"https://{label}.sharepoint.com" if label else ""


def _short(url: str) -> str:
    """A site without its scheme: what a sentence can carry, and what a person can type."""
    return url.split("://", 1)[-1].rstrip("/")


def _site_of(audience: str, wanted: "str | None" = None) -> str:
    """The site a command would reach, short, for a sentence that has to name it."""
    entry = _load().get(audience) or {}
    if wanted:
        try:
            return _short(_address(audience, entry, wanted))
        except LookupError:
            return wanted
    return _short(_current(audience, entry))


def _known_sites(audience: str) -> "list[tuple[str, str]]":
    """The sites this session remembers, under the short name a ``use`` accepts."""
    entry = _load().get(audience) or {}
    answer = []
    for site in entry.get("contexts", []):
        url = str(site.get("url", "")).rstrip("/")
        if not url:
            continue
        answer.append((str(site.get("name") or _site_name(url)), str(site.get("title") or _short(url))))
    return answer


def _refuse(message: str, code: int = 2) -> int:
    """Say why nothing ran, and answer the shell with a non-zero code."""
    print(f"o365: {message}", file=sys.stderr)
    return code


def licences(argv: "list[str]") -> int:
    """Which licences a command names, and whether this tenant holds them.

    Two reads, the two :class:`~office365.licensing.guard.LicenceGuard` makes: what the tenant
    bought (``subscribedSkus``) and, for a licence whose seat is the caller, what is assigned to
    them. The words come from ``office365/index.json``, which carries each noun's own marker, so
    the vocabulary here is the declaration's rather than a list kept beside it - a stamp added to
    a type shows up in this table once the index is re-rendered, and nothing else changes.
    """
    from office365.licensing.report import COLUMNS, headline, of, rows
    from office365.runtime.client_request_exception import ClientRequestException
    from office365.runtime.render import render

    parser = argparse.ArgumentParser(
        prog="o365 licences", description="Which licences a command names, and whether this tenant holds them"
    )
    parser.add_argument("-o", "--output", choices=LICENCE_FORMATS, default="table", help="what to print")
    args = parser.parse_args(argv)
    declared = of(json.loads(INDEX.read_text("utf-8")))
    if not declared:
        print("no type in this library declares a licence")
        return 0
    try:
        client = _client("graph")
        held = client.licences.get_all().execute_query().value
    except LookupError as error:
        return _refuse(str(error))
    except ClientRequestException as error:
        return _refuse(f"the tenant's subscriptions could not be read: {error}", 1)
    tenant = client.tenant_name or ""
    records = rows(declared, held.plans, _assigned(client))
    sentence = headline(records, tenant)
    if args.output == "json":
        print(sentence, file=sys.stderr)
        print(json.dumps({"tenant": tenant, "held": sorted(held.plans), "licences": records}, indent=2))
        return 0
    if args.output in PIPED_FORMATS:
        print(sentence, file=sys.stderr)
        print(render(records, args.output, columns=COLUMNS))
        return 0
    print(sentence)
    print()
    print(render(records, args.output, columns=COLUMNS))
    return 0


def _assigned(client: Any) -> "frozenset[str] | None":
    """The plans assigned to the calling identity, or ``None`` when that read was not made.

    A seat is a fact about the person making the call, so it costs a second read; a token
    without ``User.Read.All`` cannot make it, and the answer is then *unknown* rather than *no* -
    an unread licence is not a missing one, and a report that said otherwise would accuse a
    tenant that paid for it.
    """
    from office365.runtime.client_request_exception import ClientRequestException

    try:
        return client.licences.get_user(client.me).execute_query().value.plans
    except (ClientRequestException, LookupError):
        return None


def _audience_words(words: "list[str]") -> tuple[str, "list[str]"]:
    """Take a leading audience word off the line, and say which session the line is about.

    An audience word is taken in two cases: a session verb follows it, so ``o365 sharepoint
    login`` is the sharepoint session and not the sharepoint product -- and ``use``/``context``
    are session verbs where a site boundary exists; or the tree has no package of that name,
    which is ``graph`` alone, so ``o365 graph directory user get`` is the directory user and
    ``o365 graph`` asks what that one token serves. ``o365 sharepoint web get`` keeps its word,
    because there is a package behind it and the word after it is a noun.
    """
    if not words or words[0] not in AUDIENCES:
        return "", words
    if len(words) > 1 and (words[1] in SESSION or (words[0] in CONTEXT_AUDIENCES and words[1] in SITE_WORDS)):
        return words[0], words[1:]
    if _is_product(words[0]):
        return "", words
    return words[0], words[1:]


def _is_product(word: str) -> bool:
    """Whether the tree has a package of that name, read without importing it."""
    return importlib.util.find_spec(f"office365.{word}") is not None


def _served(audience: str) -> str:
    """What one token answers, when no product or verb follows it."""
    served = [name for name in _published() if name not in AUDIENCES]
    return f"{audience} serves {len(served)} products: " + ", ".join(served)


def _published() -> "list[str]":
    """The products the tree publishes, read from the index; the packages answer if it is gone.

    The import is the fallback, not the first attempt: it is one ``find_spec`` per package
    (0.18 s measured here) for a list the index already holds, and the index is what keeps
    ``o365 graph`` at 0.05 s.
    """
    try:
        return sorted(json.loads(INDEX.read_text("utf-8"))["products"])
    except (OSError, ValueError, KeyError):
        from office365.routing import products

        return list(products())


def _complete(argv: "list[str]") -> int:
    """Answer a shell: the words that may follow, one per line, a description after a tab.

    The shell passes the words already on the line and the word under the cursor, because only
    it knows where the cursor is. The two protocol flags are read by hand rather than by
    ``argparse``, because a word of this command line may itself begin with ``-`` (``list -o``)
    and an option parser would take it for an option of the completer. A flag this command line
    does not know is passed on as a word rather than refused: it is something the user has
    already typed, and a TAB that failed would delete it.
    """
    prefix, describe, words = "", False, []
    rest = list(argv)
    while rest:
        word = rest.pop(0)
        if word == "--describe":
            describe = True
        elif word == "--prefix":
            prefix = rest.pop(0) if rest else ""
        elif word.startswith("--prefix="):
            prefix = word.split("=", 1)[1]
        else:
            words.append(word)
    for word, detail in _following(words, prefix):
        print(f"{word}\t{detail}" if describe else word)
    return 0


def _following(words: "list[str]", prefix: str) -> "list[tuple[str, str]]":
    """The words that may follow these, filtered by the one being typed.

    Three shapes, because a command line has three: nothing, a product, and whatever the route
    reached. The command line's own words - the products, the session verbs, the flags of a
    command - are answered here, before any package is imported, and the model's words are
    asked of :mod:`office365.completion`, which caches them. A path the router refuses answers
    nothing rather than offering a word the walk cannot reach.
    """
    if not words:
        return _prefixed(_top(), prefix)
    head, rest = words[0], words[1:]
    if not (_is_product(head) or head in AUDIENCES):
        return []
    if not rest and head in AUDIENCES:
        # The session's own words come first: `o365 sharepoint login` is the question a person
        # asks before any noun, and the model's nouns are long enough to bury it.
        return _prefixed(_sessions() + _context_words(head) + _after(head, rest), prefix)
    return _prefixed(_after(head, rest), prefix)


def _context_words(audience: str) -> "list[tuple[str, str]]":
    """The two words that move a session's site boundary, for the audiences that have one."""
    if audience not in CONTEXT_AUDIENCES:
        return []
    return [("use", "address another site"), ("context", "where this session is addressed")]


def _after(product: str, path: "list[str]") -> "list[tuple[str, str]]":
    """What may follow ``<product> <path>``: nouns, a route's words, or a command's flags."""
    if product in CONTEXT_AUDIENCES and path[:1] == ["use"]:
        return _known_sites(product)
    if product in CONTEXT_AUDIENCES and path[:1] == ["context"]:
        if len(path) > 1 and path[1] == "use":
            return _known_sites(product)
        return [
            ("ls", "the sites this session remembers"),
            ("use", "address another site"),
            ("inspect", "the site it is addressed at"),
        ]
    from office365.completion import following

    cut = next((position for position, item in enumerate(path) if item.startswith("-")), len(path))
    walk, typed = path[:cut], path[cut:]
    if typed:
        return _values(product, walk, typed)
    try:
        node = following(product, walk)
    except LookupError:
        return []
    if node is not None:
        return [(candidate.word, candidate.detail) for candidate in node]
    from office365.routing import route

    return _flag_words(route(product, *walk))


def _top() -> "list[tuple[str, str]]":
    """Nothing typed yet: what owns a token, what owns types, and the two words with no noun."""
    return (
        [(name, "audience") for name in AUDIENCES]
        + _products()
        + _sessions()
        + [("completion", "shell script"), ("licences", "what this tenant holds"), ("help", "any of these pages")]
    )


def _products() -> "list[tuple[str, str]]":
    """The products a token answers, minus the ones that are audiences and so already offered."""
    return [(name, "product") for name in _published() if name not in AUDIENCES]


def _sessions() -> "list[tuple[str, str]]":
    """The verbs that speak to the session rather than to the service."""
    return [(name, "session") for name in SESSION]


def _flag_words(found: Any) -> "list[tuple[str, str]]":
    """The flags a command takes: its own parameters, then what every command prints with."""
    method = getattr(found.here or found.entity, found.method)
    answer = []
    for name, parameter in _signature(method).parameters.items():
        if name in SUPPLIED or parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            continue
        answer.append(("--" + name.replace("_", "-"), getattr(_unoptional(parameter.annotation), "__name__", "")))
    return (
        answer
        + [
            ("-o", "the format to print"),
            ("--output", "the format to print"),
            ("--columns", "the names the table shows"),
            ("--no-headers", "rows without the header line"),
            ("--link", "when a name carries its URL"),
            ("--yes", "send a destroy action without asking"),
            ("--dry-run", "print the request and send nothing"),
        ]
        + (
            [("-s", "another site for this command"), ("--site", "another site for this command")]
            if _audience(found.entity) in CONTEXT_AUDIENCES
            else []
        )
    )


def _values(product: str, walk: "list[str]", typed: "list[str]") -> "list[tuple[str, str]]":
    """The values a flag takes, when the line stopped on that flag's name."""
    if typed[-1] in ("-o", "--output"):
        from office365.runtime.render import FORMATS

        told = {
            "table": "the columns a reader wants",
            "wide": "every field the payload carried",
            "json": "the payload as it came",
            "csv": "for a spreadsheet",
            "tsv": "for a spreadsheet, tab separated",
            "url": "one address per line",
            "name": "one name per line",
        }
        return [(fmt, told.get(fmt, "")) for fmt in FORMATS]
    if typed[-1] in ("-s", "--site") and walk:
        return _known_sites(product)
    if typed[-1] == "--link":
        return [("auto", "when printing to a terminal"), ("always", "even into a pipe"), ("never", "plain text")]
    if typed[-1] == "--columns" and walk:
        from office365.routing import route
        from office365.runtime.schema import TypeSchema

        try:
            found = route(product, *walk)
        except LookupError:
            return []
        return [(name, "") for name in TypeSchema.of(found.entity).columns]
    return []


def _prefixed(pairs: "list[tuple[str, str]]", prefix: str) -> "list[tuple[str, str]]":
    """Keep the words that start with what is being typed, once, in the order they were offered."""
    seen: "set[str]" = set()
    answer = []
    for word, detail in pairs:
        if word.startswith(prefix) and word not in seen:
            seen.add(word)
            answer.append((word, detail))
    return answer


def _completion(argv: "list[str]") -> int:
    """Print a shell's completion script, or fill the cache so that no TAB pays an import."""
    from office365 import completion

    words = list(argv)
    if "--warm" in words:
        words.remove("--warm")
        try:
            answered = completion.warm(words or _published())
        except LookupError as err:
            return _refuse(str(err))
        print(f"{answered} nouns answered -> {completion.cache_path()}")
        return 0
    if not words:
        print("usage: o365 completion bash|zsh|fish [--warm [product ...]]")
        return 0
    try:
        print(completion.script(words[0]), end="")
    except LookupError as err:
        return _refuse(str(err))
    return 0


def _help(audience: str, words: "list[str]") -> int:
    """``o365 help <product> <noun> ...``: the page a route answers, or the arguments of a leaf.

    It goes through :func:`command` with ``-h`` so that one place decides what a route means:
    a node prints its page, an action prints the flags of the method the route reached. A
    person who typed ``o365 help sharepoint web lists list`` gets the same text as
    ``o365 sharepoint web lists list -h``, which is what ``kubectl help`` and ``docker help`` do.
    """
    spoken = list(words)
    if spoken and (spoken[0] in AUDIENCES or _is_product(spoken[0])):
        product, spoken = spoken[0], spoken[1:]
    elif audience:
        product = audience
    else:
        print(_usage(), file=sys.stderr)
        return 2
    if not spoken:
        print(_served(product))
        return 0
    try:
        return command(product, spoken, ["-h"])
    except SystemExit as stop:  # argparse answers -h with the code it promises
        return int(stop.code or 0)


def command(product: str, words: "list[str]", argv: "list[str]") -> int:
    """Run ``<product> <noun> [navigation ...] [action]``: the words are the route, the flags are
    the method's own.
    """
    from office365.routing import chain, route

    spoken = " ".join(words)
    try:
        found = route(product, *words)
    except LookupError as err:
        return _refuse(str(err))
    if found.verb is None:
        print(_page(product, spoken, found))
        return 0
    target = found.here
    if target is None:
        return _refuse(f"{product} {spoken} does not answer {words[-1]!r}")
    method = getattr(target, found.method)
    # The walk reads types only, so the route to the noun is known before a token is: help and
    # a bad flag are answered without a session, and only the request itself needs one.
    path = chain(_root(_audience(found.entity)), found.entity)
    walk = path + found.walk if path is not None else None
    parser = argparse.ArgumentParser(
        prog=f"o365 {product} {spoken}",
        description=f"Walk {' -> '.join(walk)}, then {found.method}() on {target.__name__}"
        if walk
        else f"{found.method}() on {target.__name__}",
        epilog="\n".join(_hints(target, found.method)),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    from office365.runtime.render import FORMATS

    _flags(parser, method, set())
    parser.add_argument("-o", "--output", choices=FORMATS, default="table", help="what to print")
    parser.add_argument("--columns", default=None, help="comma separated names the table shows")
    parser.add_argument("--no-headers", action="store_true", help="print rows without the header line")
    parser.add_argument(
        "--link", choices=("auto", "always", "never"), default="auto", help="when a name carries its URL"
    )
    if "base_url" in _signature(_root(_audience(found.entity))).parameters:
        parser.add_argument(
            "-s",
            "--site",
            default=os.environ.get("O365_SITE") or None,
            help="address another site for this command only (default: $O365_SITE)",
        )
    parser.add_argument("-y", "--yes", action="store_true", help="send a destroy action without asking")
    parser.add_argument("-n", "--dry-run", action="store_true", help="print the request and send nothing")
    args = parser.parse_args(argv)
    given = _accepted(args, method)
    # A destroy action is the one that asks, and `confirm` is derived from the effect, so this
    # gate cannot drift from the effect the page printed. It sits before the session is read:
    # "may I?" is answerable with no token, and a refusal costs no request.
    if found.verb.confirm and not (args.yes or args.dry_run):
        # The site is named because "which one" is the mistake a destroy action cannot undo.
        where = _site_of(_audience(found.entity), getattr(args, "site", None))
        return _refuse(
            f"`{words[-1]}`" + (f" on {where}" if where else "") + " destroys what the service holds;"
            " send it again with --yes"
        )

    try:
        client = _client(_audience(found.entity), live=not args.dry_run, site=getattr(args, "site", None))
    except LookupError as err:
        return _refuse(str(err))
    if walk is None:
        return _refuse(
            f"{product} {spoken} is declared, but nothing walks there from {type(client).__name__}:"
            " every link on the way needs an argument the model does not name yet"
        )
    noun = found.walk[-1] if found.walk else found.noun
    return _send(
        client,
        getattr(functools.reduce(getattr, walk, client), found.method),
        given,
        args,
        found.shows,
        empty=f"No {noun} found.",
    )


def _hints(target: Any, method: str) -> "list[str]":
    """What to know before sending this command: its permission, its licence, its beta root.

    The five facts are already declared and are joined by :func:`office365.capabilities.hints_of`;
    this asks it rather than restating any of them, so a sentence can never appear here that the
    model does not say. A target that declares no verb answers nothing: ``-h`` is still the help
    page for its flags, and an invented sentence would be worse than a missing one.
    """
    from office365.capabilities import hints_of

    try:
        return list(hints_of(target, method))
    except (TypeError, ValueError):
        return []


#: What a role does, in the words a command line uses. A role is a closed vocabulary in the
#: model (``ROLES``), so its sentence belongs here, once -- writing it on 4,000 methods would
#: be 4,000 places to keep in step. An ``action`` has no sentence of its own: it is the
#: service's operation, and its docstring (written by the generator from the metadata's own
#: summary) is the only text that says what it does.
_ROLE_SENTENCE = {
    "get": "read this one back",
    "list": "read every one it holds",
    "create": "create one here",
    "update": "change what you name",
    "delete": "remove this one",
    "action": "",
}

#: The order actions are shown in, and the heading each group gets. Effects are declared, not
#: inferred from a spelling here, so a destructive action can never be listed as a read.
_EFFECTS = (("read", "READ"), ("write", "WRITE"), ("destroy", "DESTROY"), ("local", "SESSION"))

#: How many links a page lists before it stops being a page; a TAB still offers all of them.
LINK_WORDS = 12

#: How wide the action-name column is allowed to get: `get-managed-app-diagnostic-statuses`
#: would otherwise push every sentence off to the right.
_WORD_WIDTH = 26

#: Where a service's one-line summary is cut: long enough for a real sentence, short enough
#: that the page stays a page.
_SENTENCE_WIDTH = 70


def _page(product: str, spoken: str, found: Any) -> str:
    """The page a node answers: what it is, what it answers, what it holds, what to type next.

    Every line is read off the model: the actions are the type's stamped verbs, the groups are
    the effect each declares, the links are the getters the walk accepts, and the columns a
    read shows are the type's ranked defaults (``-o wide`` shows every field the payload
    carried). So nothing here is a vocabulary someone has to keep in step with the library.
    """
    from office365.permissions.declaration import TENANT, licence_of
    from office365.routing import navigations
    from office365.runtime.schema import TypeSchema

    here = found.here or found.entity
    schema = TypeSchema.of(found.shows)
    lines = [f"{product} {spoken} \u2014 {found.shows.__name__}"]
    if schema.defaults:
        lines.append(f"  a read shows {', '.join(schema.defaults)}")
    licence = licence_of(found.shows) or licence_of(here)
    if licence is not None and licence.plans:
        # Any one of them carries the capability; the licence is declared on the type, so the
        # page says it once rather than on each of the actions below - and says whose seat has
        # to hold it, because a per-person capability fails for a different reason.
        seat = "" if licence.seat == TENANT else " (assigned to you)"
        lines.append(f"  needs a licence: {', '.join(licence.plans)}{seat}")
    width = min(max((len(word) for word in found.commands), default=0), _WORD_WIDTH)
    for effect, title in _EFFECTS:
        rows = [
            (word, _sentence(half, method, meta))
            for word, (half, method, meta) in sorted(found.commands.items())
            if meta.effect == effect
        ]
        if not rows:
            continue
        lines.append("")
        lines.append(title)
        for word, sentence in rows:
            if len(word) > width:
                # A word past the column keeps its sentence on the next line rather than
                # pushing every other row's text out of line.
                lines.append(f"  {word}".rstrip())
                if sentence:
                    lines.append(f"      {sentence}")
            else:
                lines.append(f"  {word.ljust(width)}  {sentence}".rstrip())
    # Shortest first: the words a person types are the short ones (`lists`, `webs`, `items`),
    # and alphabetical order would spend the twelve on `access_requests_list`.
    links = sorted((word for word in navigations(here) if word not in found.commands), key=lambda w: (len(w), w))
    if links:
        lines.append("")
        lines.append("LINK")
        shown = links[:LINK_WORDS]
        lines.extend("  " + line for line in textwrap.wrap("  ".join(shown), width=76) or [""])
        if len(links) > len(shown):
            lines.append(f"  \u2026and {len(links) - len(shown)} more; a TAB offers every one")
    lines.append("")
    lines.append("TRY")
    lines.extend("  " + line for line in _examples(product, spoken, found, links))
    lines.append("")
    lines.append("  every action answers -h  \u00b7  -o json|csv|url prints it for a program")
    return "\n".join(lines)


def _sentence(half: type, method: str, meta: Any) -> str:
    """The one line that says what an action does: the service's summary, or the role's sentence."""
    if meta.role != "action":
        return _ROLE_SENTENCE.get(meta.role, "")
    declared = (inspect.getdoc(getattr(half, method, None)) or "").split("\n")[0].strip().rstrip(".")
    # A docstring that opens with a block header (`Requires permissions:`) has no summary of
    # its own, and printing the header alone would say nothing.
    if not declared or declared.endswith(":"):
        return ""
    return declared[: _SENTENCE_WIDTH - 1] + "\u2026" if len(declared) > _SENTENCE_WIDTH else declared


def _examples(product: str, spoken: str, found: Any, links: "list[str]") -> "list[str]":
    """Two lines worth copying: a read of this node, and a word deeper into the model."""
    from office365.runtime.schema import TypeSchema

    examples = []
    for word in ("get", "list"):
        if word not in found.commands:
            continue
        columns = TypeSchema.of(found.shows).defaults
        flags = f" --columns {','.join(columns)}" if word == "list" and columns else ""
        examples.append(f"o365 {product} {spoken} {word}{flags}")
    if not examples and found.commands:
        examples.append(f"o365 {product} {spoken} {sorted(found.commands)[0]}")
    examples.extend(f"o365 {product} {spoken} {word} list" for word in _feeds(product, spoken, links, 2))
    return examples


def _feeds(product: str, spoken: str, links: "list[str]", wanted: int) -> "list[str]":
    """The first links that answer ``list`` themselves, so the example reads something back.

    A link that is a single object would make ``... folders`` an example of walking nowhere;
    the feed is the one a reader wants, and the model already says which links are one.
    """
    from office365.routing import route

    found = []
    for word in sorted(links, key=lambda word: (len(word), word)):
        try:
            deeper = route(product, *spoken.split(" "), word)
        except LookupError:
            continue
        if "list" in deeper.commands:
            found.append(word)
            if len(found) == wanted:
                break
    return found or links[:wanted]


def _send(
    client: Any,
    method: Any,
    given: "Mapping[str, Any]",
    args: argparse.Namespace,
    entity: type,
    *,
    empty: str = "",
) -> int:
    """Call the method, run the one query it queued, and print what came back.

    The table is rendered by :mod:`office365.runtime.render` rather than by the notebook's
    ``describe_collection``: a terminal wants a header row, aligned numbers and a link, and
    a repr wants to be bounded and indented. Which fields are a link is the type's answer
    (``TypeSchema.links``, the ``link`` facet), not a list of spellings kept here.
    """
    from office365.runtime.client_request_exception import ClientRequestException
    from office365.runtime.render import render
    from office365.runtime.schema import TypeSchema

    result = method(**given)
    asked = _asked_for(args, entity)
    if asked and _can_select(result):
        result.select(asked)
    if args.dry_run:
        print(_preview(client))
        return 0
    try:
        client.execute_query()
    except ClientRequestException as err:
        return _refuse(str(err), 1)
    rows = _rows(result)
    records = [_payload(row) for row in rows]
    # One object is a block of its own fields, not a table of one row: a single `Title` under a
    # `TITLE` heading says less than every field on its own line. A feed of one item is still a
    # feed -- `item_type` is what tells the two apart -- and naming columns is a table on purpose.
    block = len(records) == 1 and not hasattr(result, "item_type")
    print(
        render(
            records,
            args.output,
            columns=None if block and not args.columns else _columns(records, args.columns, entity),
            links=None,
            origin=render_origin(client),
            resources=_addresses(rows),
            fields=TypeSchema.of(entity).links,
            link=args.link,
            headers=not args.no_headers,
            tty=sys.stdout.isatty(),
            empty=empty,
        )
    )
    return 0


def _preview(client: Any) -> str:
    """The requests the method queued, as they would be sent: method, URL, and any body.

    Built by the request class the session already uses, so the preview cannot describe a
    request the client would not send -- the version, the path and the payload are its answer.
    Authentication is not run, which is what makes this printable before a token is read.
    """
    request = client.pending_request()
    lines = []
    for query in client.queries:
        built = request.build_request(query)
        lines.append(f"{built.method.value} {built.url}")
        if built.data:
            body = built.data if isinstance(built.data, str) else json.dumps(built.data, indent=2, default=str)
            lines.extend("  " + line for line in body.splitlines())
    return "\n".join(lines)


def _asked_for(args: argparse.Namespace, entity: type) -> "list[str]":
    """The fields the request must ask for, empty when it should take what the service sends.

    A table needs the columns it prints and the address it links to, and SharePoint leaves some
    of them out of an unselected payload: ``/Web/lists`` answers without ``DefaultViewUrl``, so
    every list name would be plain text. ``-o json`` and ``-o wide`` ask for nothing -- a caller
    reading everything is reading what the service chose to send, not our idea of a table.
    """
    from office365.runtime.schema import TypeSchema

    schema = TypeSchema.of(entity)
    chosen = getattr(args, "columns", None)
    if not chosen:
        if getattr(args, "output", "table") in ("json", "wide"):
            return []
        chosen = ",".join(schema.reading)
    # `--columns title,itemcount` prints, because `_columns` reads the payload without regard to
    # case; `$select` does not, so the spelling a `$select` needs is restored here.
    spelled = {name.lower(): name for name in schema.columns}
    named = [spelled.get(one.strip().lower(), one.strip()) for one in chosen.split(",") if one.strip()]
    return list(dict.fromkeys([*named, *schema.links]))


def _can_select(result: Any) -> bool:
    """Whether this answer is a feed that has not been narrowed yet.

    A feed that declares it refuses ``$select`` is left alone: the table then prints what the
    service sends, which is exactly what it did before anyone asked, and the declaration stays
    the one place that says so.
    """
    from office365.runtime.query_capabilities import query_capabilities_of

    options = getattr(result, "query_options", None)
    if options is None or not callable(getattr(result, "select", None)):
        return False
    if options.select:
        return False
    capability = query_capabilities_of(type(result))
    return capability is None or capability.supports("$select")


def render_origin(client: Any) -> str:
    """``scheme://host`` for the server-relative links a SharePoint payload carries."""
    from office365.runtime.render import origin_of

    return origin_of(getattr(client, "service_root_url", None))


def _addresses(rows: "list[Any]") -> "list[str | None]":
    """Each row's own REST address -- one per row, so it lines up with the record it belongs to."""
    return [None if isinstance(row, Mapping) else getattr(row, "resource_url", None) for row in rows]


def _payload(row: Any) -> "Mapping[str, Any]":
    """One row as what a table reads: the object's own JSON, or a value under ``value``."""
    payload = row.to_json() if hasattr(row, "to_json") else row
    return payload if isinstance(payload, Mapping) else {"value": payload}


def _columns(records: "list[Any]", chosen: "str | None", entity: type) -> "list[str] | None":
    """The columns a table shows: the ones asked for, or the ones the type says a reader wants."""
    if chosen:
        return [name.strip() for name in chosen.split(",") if name.strip()]
    from office365.runtime.schema import TypeSchema

    spelled = {name.lower(): name for name in sorted({name for r in records if isinstance(r, Mapping) for name in r})}
    wanted = TypeSchema.of(entity).defaults
    return [spelled[name.lower()] for name in wanted if name.lower() in spelled] or None


def _rows(result: Any) -> "list[Any]":
    """What a command prints, one entry per row: a collection's items, or the one object.

    The items and not their JSON, because a row needs both halves: the payload the table
    reads and the REST address the row links to. ``to_json()`` on a collection has only the
    first, which is how a table of 146 lists came out with no addresses.
    """
    if isinstance(result, (list, tuple)):
        return list(result)
    if isinstance(result, Mapping):
        return [result]
    if hasattr(result, "item_type") and hasattr(result, "to_json"):
        # Only a collection is a feed. An entity iterates its own fields as ``(name, value,
        # stated)`` triples -- that is what a request carries -- so iterating a ``Web`` would
        # print one row per field: `["Title", "SiteU74H3Z9O", false]` under a `VALUE` heading.
        return [item for item in result] or [result]
    if hasattr(result, "to_json"):
        # A result whose own JSON is the table (`Report` over a CSV answer) is already rows.
        payload = result.to_json()
        return list(payload) if isinstance(payload, list) else [result]
    return [result]


def _audience(entity: type) -> str:
    """Which token reads a type: its product, when the product is an audience of its own.

    ``sharepoint`` is an audience and a product; ``outlook`` and 20 more are only products, all
    served by one token. No MRO is walked, so a shared base cannot mislead.
    """
    from office365.runtime.schema import TypeSchema

    product = TypeSchema.of(entity).product
    return product if product in AUDIENCES else "graph"


def _client(audience: str, live: bool = True, site: "str | None" = None) -> Any:
    """A client for ``audience``, holding the token its session kept.

    A command does not log in: it either finds a live token in the store or says to run
    ``login`` again. Re-running the mode would need the credentials a session must not
    keep - the second half of ``username-and-password`` was missing on the first live run.
    """
    entry = _load().get(audience)
    if entry is None:
        ran = "o365 login" if audience == "graph" else f"o365 {audience} login"
        raise LookupError(f"no session for {audience}; run {ran}")
    constructor = dict(entry["constructor"])
    if "base_url" in constructor:
        # The site is the boundary: this command addresses one site collection, and `use` or
        # `--site` says which. What login was given is the answer until one is chosen.
        wanted = site or _current(audience, entry)
        if wanted:
            constructor["base_url"] = _address(audience, entry, wanted)
    client = _root(audience)(**constructor)
    if not live:
        # `--dry-run` prints the request the client would send, and building it reads the
        # path and the payload but no token -- so a stale session can still be inspected.
        return client
    token = _token(entry)
    # The OAuth response shape, not just the secret: a provider reads the scheme too.
    client.pending_request().with_access_token(lambda: {"access_token": token, "token_type": "Bearer"})
    return client


def _token(entry: "Mapping[str, Any]") -> str:
    """The access token the session still holds; nothing here refreshes it."""
    kept = entry.get("token") or {}
    if int(kept.get("expires_on", 0)) > time.time():
        return kept["access_token"]
    tokens = json.loads(entry.get("cache") or "{}").get("AccessToken", {})
    live = [token for token in tokens.values() if int(token.get("expires_on", 0)) > time.time()]
    if not live:
        raise LookupError(f"the {entry['mode']} session has no live token here; run login again")
    return max(live, key=lambda token: int(token["expires_on"]))["secret"]


def _root(audience: str) -> type:
    """The client class that owns the audience's token."""
    from office365.runtime.client_runtime_context import ClientRuntimeContext

    module = importlib.import_module(AUDIENCES[audience])
    roots = [
        member
        for member in vars(module).values()
        if isinstance(member, type) and issubclass(member, ClientRuntimeContext) and member is not ClientRuntimeContext
    ]
    return min(roots, key=lambda root: root.__module__.count("."))


def _flags(parser: argparse.ArgumentParser, fn: Any, seen: "set[str]") -> None:
    """Declare one flag per parameter ``fn`` takes, except the supplied ones."""
    for name, parameter in _signature(fn).parameters.items():
        if name in seen or name in SUPPLIED or parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            continue
        seen.add(name)
        annotation = _unoptional(parameter.annotation)
        kwargs: "dict[str, Any]" = {"dest": name, "default": argparse.SUPPRESS}
        if annotation is bool:
            kwargs["action"] = "store_true"
        elif get_origin(annotation) is list:
            kwargs["nargs"] = "+"
        elif isinstance(annotation, type) and issubclass(annotation, Enum):
            kwargs["choices"] = [member.value for member in annotation]
        parser.add_argument("--" + name.replace("_", "-"), **kwargs)


def _accepted(args: argparse.Namespace, fn: Any) -> "dict[str, Any]":
    """The arguments ``fn`` declares, converted back to what it asks for."""
    parameters = _signature(fn).parameters
    accepted: "dict[str, Any]" = {}
    for name, value in vars(args).items():
        if name not in parameters:
            continue
        annotation = _unoptional(parameters[name].annotation)
        accepted[name] = annotation(value) if isinstance(annotation, type) and issubclass(annotation, Enum) else value
    return accepted


def _signature(fn: Any) -> inspect.Signature:
    """``fn``'s signature with annotations evaluated, or as written if a name is unimportable."""
    try:
        return inspect.signature(fn, eval_str=True)
    except NameError:
        return inspect.signature(fn)


def _unoptional(annotation: Any) -> Any:
    """``Optional[str]`` -> ``str``: a flag cannot mean two types."""
    if get_origin(annotation) in (Union, types.UnionType):
        rest = [argument for argument in get_args(annotation) if argument is not type(None)]
        return rest[0] if rest else str
    return annotation


def _store() -> Path:
    """Where the sessions live; ``O365_HOME`` overrides the default directory."""
    home = os.environ.get("O365_HOME") or str(Path.home() / ".o365")
    return Path(home) / "sessions.json"


def _config() -> Path:
    """What has to be answered once rather than every run; ``O365_HOME`` overrides it too."""
    home = os.environ.get("O365_HOME") or str(Path.home() / ".o365")
    return Path(home) / "config.json"


def _prefs() -> "dict[str, str]":
    """The config file, read and never written: a client id and a site are the person's, not ours.

    A session is a secret and lives in the store, writable by this command and readable only by
    its owner; a preference is not a secret and this command has no business editing your file.
    """
    try:
        kept = json.loads(_config().read_text("utf-8"))
    except (OSError, ValueError):
        return {}
    return {name: str(value) for name, value in kept.items() if isinstance(value, (str, int))}


def _load() -> "dict[str, Any]":
    """Every kept session, or nothing when there is no readable store."""
    try:
        return json.loads(_store().read_text("utf-8"))
    except (OSError, ValueError):
        return {}


def _save(sessions: "dict[str, Any]") -> None:
    """Write the store readable only by its owner."""
    path = _store()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sessions, indent=2), "utf-8")
    path.chmod(0o600)


def _claims(access_token: str) -> "dict[str, Any]":
    """What the token says about itself - a decode, not a verification, because this only reports."""
    try:
        payload = access_token.split(".")[1]
        data = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    except (IndexError, ValueError):
        return {}
    names = ("preferred_username", "upn", "appid", "tid", "scp", "roles", "exp")
    return {name: data[name] for name in names if name in data}


def _summary(audience: str, entry: "dict[str, Any]") -> str:
    """One line of who the session is, and whether it still holds."""
    claims = entry.get("claims") or {}
    who = claims.get("preferred_username") or claims.get("upn") or claims.get("appid") or "<unknown>"
    grants = claims.get("scp") or " ".join(claims.get("roles") or []) or "-"
    expires = int(claims.get("exp") or 0)
    left = "" if not expires else f", {max(0, expires - int(time.time())) // 60} min left"
    state = f" (expired; run o365 {audience} login)" if expires and expires < time.time() else left
    line = f"{audience}: {who} (tenant {claims.get('tid', '-')}, mode {entry['mode']}{state})\n  grants: {grants}"
    site = _current(audience, entry)
    if site:
        remembered = next(
            (held.get("title", "") for held in entry.get("contexts", []) if held.get("url", "").rstrip("/") == site), ""
        )
        line += f"\n  at {_short(site)}" + (f" — {remembered}" if remembered else "")
    return line


def _usage() -> str:
    """What this command line knows: a session, a route of words, and the shell script."""
    return (
        "usage: o365 [graph|sharepoint|exchange] login|whoami|logout [flags]\n"
        "       o365 <product> <noun> [navigation ...] [action] [flags]\n"
        "       o365 <product> <noun> list [-o table|wide|json|csv|tsv|url|name]\n"
        "       o365 <product> <noun> ... delete [--yes] [-n|--dry-run]\n"
        "       o365 graph <product> <noun> [navigation ...] [action]\n"
        "       o365 login [--tenant <tenant>] [--client-id <id>] [--mode device-flow] [--scopes ...]\n"
        "       o365 sharepoint use <site> [--as <name>]   (a site is one ClientContext)\n"
        "       o365 sharepoint context [ls|use <name>|inspect]\n"
        "       o365 completion bash|zsh|fish [--warm [product ...]]\n"
        "       o365 licences [-o table|wide|csv|tsv|json]\n"
        "  a flag falls back to O365_CLIENT_ID/O365_TENANT/O365_SITE, then to ~/.o365/config.json"
    )


def _plain(value: Any) -> Any:
    """A constructor argument as JSON can keep it."""
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return [_plain(item) for item in value]
    return value


if __name__ == "__main__":
    raise SystemExit(main())
