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
    o365 config [<key>]                 -- what a login reads, and the file to edit
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
``O365_CLIENT_ID``/``O365_TENANT``/``O365_SITE``, then the file, then a block that prints the file
to write -- and ``o365 config`` says what is answered already and which of the four answered it.
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
import shutil
import sys
import textwrap
import time
import types
from collections.abc import Callable, Mapping, Sequence
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, NamedTuple, TypedDict, Union, get_args, get_origin
from urllib.parse import urlparse

if TYPE_CHECKING:
    from office365.graph_client import GraphClient
    from office365.licensing.report import LicenceRecord
    from office365.permissions.token import TokenClaims
    from office365.routing import Route
    from office365.runtime.client_runtime_context import ClientRuntimeContext

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


class Setting(NamedTuple):
    """One fact a login reads from the person rather than from the arguments of one run.

    ``key`` is its name in ``config.json``, ``spoken`` how it reads in a sentence, and the two
    shortcuts answer it for one shell or one command; the file answers it for every later run.
    """

    key: str
    spoken: str
    env: str
    flag: str


#: What a login has to be told once, in the order a person meets it: which directory, which
#: application, then which site collection.
SETTINGS = (
    Setting("tenant", "tenant", "O365_TENANT", "--tenant"),
    Setting("client_id", "client id", "O365_CLIENT_ID", "--client-id"),
    Setting("site", "site", "O365_SITE", "--base-url"),
)

#: What each setting looks like when the file is written from scratch. Two are examples; the
#: client id is marked, because it is the one answer this library cannot know or supply.
EXAMPLES = {
    "tenant": "contoso.onmicrosoft.com",
    "client_id": "<application (client) id>",
    "site": "https://contoso.sharepoint.com/sites/team",
}

#: What a table prints in place of a value nobody answered yet, as `aws configure list` does.
NOT_SET = "<not set>"

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


class Site(TypedDict, total=False):
    """One site collection a session remembers: the address, its name, and the title it answers to."""

    url: str
    name: str
    title: str


class KeptToken(TypedDict, total=False):
    """The access token a session keeps, and when it stops being one."""

    access_token: str
    expires_on: int


class Session(TypedDict, total=False):
    """One audience's session, as ``sessions.json`` keeps it.

    Every field is optional because the store is written by whichever login ran, and because it
    outlives the version that wrote it: an entry from before sites were remembered has no
    ``contexts``, and one whose root has no cache has no ``cache``. A reader treats an absent
    field as an answer, never as a missing key -- so ``_kept_session`` is the empty one.
    """

    mode: str
    constructor: dict[str, object]
    method: str
    client_id: str
    contexts: list[Site]
    current: str
    claims: dict[str, Any]  # a decoded token payload: the claims' own shape, not ours
    token: KeptToken
    cache: str


#: The whole store, keyed by audience: one token each, so one session each.
Sessions = dict[str, Session]


def main(argv: "list[str] | None" = None) -> int:
    """Run one command, returning the process exit code."""
    words = list(sys.argv[1:] if argv is None else argv)
    # The completion protocol is answered before the grammar is read: a shell asks with the
    # words already typed, which are not a command, and asks a hundred times an hour.
    if words[:1] == ["__complete"]:
        return _complete(words[1:])
    if words[:1] == ["completion"]:
        return _completion(words[1:])
    # `config`, `licences` and `doctor` answer a question about the whole library rather than
    # about one product, so they are answered before a product is looked for.
    if words[:1] == ["config"]:
        return config(words[1:])
    if words[:1] == ["licences"]:
        return licences(words[1:])
    if words[:1] == ["doctor"]:
        return doctor(words[1:])
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
        return _refuse(_advice(["client_id"]))
    tenant = given.get("tenant") or os.environ.get("O365_TENANT") or prefs.get("tenant", "")
    if tenant and "tenant" in wanted:
        given["tenant"] = tenant
    if "base_url" in wanted and not given.get("base_url"):
        given["base_url"] = _site_for(given.get("tenant", ""), prefs)
        if not given["base_url"]:
            return _refuse(_advice(["site"]))

    import msal

    # The session file *is* the cache, and it is read back: a cache that is only ever written
    # renews nothing, so every login would show a device code for a token MSAL could have
    # renewed from the refresh token the store already held.
    kept = _kept_session(audience)
    wants_cache = any("token_cache" in _signature(fn).parameters for fn in (root, getattr(root, method)))
    cache = None
    if wants_cache:
        cache = msal.SerializableTokenCache()
        stored = kept.get("cache") or ""
        if stored:
            cache.deserialize(stored)
        given["token_cache"] = cache

    constructor = {name: value for name, value in given.items() if name in _signature(root).parameters}
    client = root(**constructor)
    getattr(client, method)(**{name: value for name, value in given.items() if name not in constructor})
    # The property both client roots state: acquired on first read, cached, never validated.
    token = client.authentication_context.access_token or ""
    claims = _claims(token)

    sessions = _load()
    kept = _remember(kept, str(constructor.get("base_url") or ""), "")
    kept.update(
        mode=args.mode,
        method=method,
        client_id=given["client_id"],
        constructor={name: _plain(value) for name, value in constructor.items() if name != "token_cache"},
        claims=claims,
        # The token itself, so an audience whose root has no cache to hold is still kept;
        # the cache beside it is what MSAL refreshes from when the root can.
        token=KeptToken(access_token=token, expires_on=int(claims.get("exp", 0))),
        cache=cache.serialize() if cache is not None else "",
    )
    sessions[audience] = kept
    _save(sessions)
    print(_welcome(audience, sessions[audience]))
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
    current = _current(entry)
    if args.word == "inspect":
        print(_inspect(audience, entry, current))
        return 0
    if args.word == "ls":
        print(_sites(entry, current, audience))
        return 0
    print(_summary(audience, entry))
    others = [site for site in entry.get("contexts", []) if _url_of(site) != current]
    if others:
        print("  also: " + ", ".join(_site_name(_url_of(site)) for site in others))
    else:
        print(f"  another site: o365 {audience} use <url>")
    return 0


def _sites(entry: Session, current: str, audience: str) -> str:
    """The sites a session remembers, the current one marked: what ``docker context ls`` prints.

    The name is what a ``use`` accepts, so it is the first column; the URL follows because two
    sites of different tenants can share a name.
    """
    remembered = [site for site in entry.get("contexts", []) if _url_of(site)]
    rows = [(_url_of(site), site.get("name", ""), site.get("title", "")) for site in remembered]
    if not rows and not current:
        return f"no sites remembered; o365 {audience} use <url>"
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


def _url_of(site: Site) -> str:
    """A remembered site's address, without the trailing slash a person may have typed."""
    return site.get("url", "").rstrip("/")


def _inspect(audience: str, entry: Session, current: str) -> str:
    """The current site, one fact per line: the address as it is sent, and the name it answers to."""
    if not current:
        return f"no site: o365 {audience} use <url>"
    held: Site = next((site for site in entry.get("contexts", []) if _url_of(site) == current), Site())
    lines = [f"site:  {current}", f"name:  {held.get('name') or _site_name(current)}"]
    if held.get("title"):
        lines.append(f"title: {held.get('title')}")
    return "\n".join(lines)


def _current(entry: Session) -> str:
    """The site a session is addressed at: the one `use` set, else what login was given."""
    return str(entry.get("current") or entry.get("constructor", {}).get("base_url") or "").rstrip("/")


def _address(audience: str, entry: Session, wanted: str) -> str:
    """A site URL from what was typed, without asking the service what sites exist.

    A remembered site answers by its title or its name, a full URL is taken as given, and a
    bare name means the site of that name under the host this session already knows -- because
    a person switching sites types ``finance``, not the tenant's hostname again.
    """
    for known in entry.get("contexts", []):
        url = _url_of(known)
        if not url:
            continue
        # A site answers to the name it was given, the one its URL spells, and its title: the
        # three things a person can remember having typed or read.
        answers = {
            known.get("name", "").lower(),
            _site_name(url).lower(),
            # The host as well as the URL, so the root site answers to ``use contoso.sharepoint.com``.
            url.split("://", 1)[-1].lower(),
            known.get("title", "").lower(),
            url.lower(),
        }
        if wanted.lower() in answers:
            return url
    if "://" in wanted:
        return wanted.rstrip("/")
    host = urlparse(_current(entry)).netloc
    if not host:
        raise LookupError(f"no site to resolve {wanted!r} against; pass a full URL")
    if "/" in wanted:
        return f"https://{host}/{wanted.strip('/')}"
    return f"https://{host}/sites/{wanted}"


def _remember(entry: Session, url: str, title: str, name: str = "") -> Session:
    """The session with ``url`` current, and first among the sites it remembers.

    The site that was current before is remembered too, even when a login wrote it and no
    ``use`` ever named it: the store's ``constructor.base_url`` is a site like any other, and
    losing it on the first switch would make the earlier answer unreachable.
    """
    url = url.rstrip("/")
    held = list(entry.get("contexts", []))
    previous = _current(entry)
    if previous and all(_url_of(site) != previous for site in held):
        held.insert(0, Site(url=previous, title=""))
    kept = [site for site in held if _url_of(site) != url]
    was = next((site for site in held if _url_of(site) == url), Site())
    # A name is kept only when it was said: the URL's last segment already answers otherwise,
    # and writing it down would make a rename look like a different site.
    chosen = name or was.get("name", "")
    here = Site(url=url, title=title or was.get("title", ""))
    if chosen:
        here["name"] = chosen
    entry["current"] = url
    entry["contexts"] = [here, *kept][:SITE_MEMORY]
    return entry


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
    entry = _kept_session("graph")
    known = str(entry.get("constructor", {}).get("tenant") or entry.get("claims", {}).get("tid") or "")
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
    entry = _kept_session(audience)
    if wanted:
        try:
            return _short(_address(audience, entry, wanted))
        except LookupError:
            return wanted
    return _short(_current(entry))


def _known_sites(audience: str) -> "list[tuple[str, str]]":
    """The sites this session remembers, under the short name a ``use`` accepts."""
    entry = _kept_session(audience)
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
    from office365.licensing.report import COUNTED_COLUMNS, headline, of, rows
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
        print(render(records, args.output, columns=COUNTED_COLUMNS))
        return 0
    print(sentence)
    print()
    print(_licence_table(records, args.output == "wide"))
    print()
    steps = [] if args.output == "wide" else [("o365 licences -o wide", "the areas each plan opens, by name")]
    print(_next([*steps, ("o365 doctor", "this session, this tenant, and what they allow")]))
    return 0


def _next(steps: "list[tuple[str, str]]") -> str:
    """The footer: the command to type next, and what it answers, aligned to the longest one.

    ``next:`` says where a reader goes from here, so it must not offer the page they are already
    looking at -- ``-o wide`` printing ``next: o365 licences -o wide`` is a page telling its
    reader to read it again. The columns are measured rather than typed, because a description
    padded by hand in a string literal is one edit away from being wrong in a way no test sees.
    """
    width = max(len(command) for command, _ in steps)
    lines = [f"next: {steps[0][0].ljust(width)}   {steps[0][1]}"]
    lines += [f"      {command.ljust(width)}   {says}" for command, says in steps[1:]]
    return "\n".join(lines)


def _licence_table(records: Sequence[LicenceRecord], wide: bool) -> str:
    """The row a reader scans, and the report a reader consults.

    Two facts decide the shape. A plan opens a list of areas, and a list is not a table cell: at
    48 columns ``INTUNE_A`` shows ``intune.devices (119), intune.print (3), intune.audit, intune.edition_upgrade…``,
    which names four of eleven and marks the rest with an ellipsis. The default counts them
    instead -- ``11`` fits every plan in this library. And ``-o wide`` must not undo that by
    putting the eleven names back into one cell, which is a paragraph the terminal wraps into
    soup: the report prints the plan once, then one line per area underneath.
    """
    from office365.licensing.report import COLUMNS, COUNTED_COLUMNS
    from office365.runtime.render import COLUMN_WIDTH, render

    if not wide:
        return render(records, "table", columns=_changing(records, COUNTED_COLUMNS), width=COLUMN_WIDTH)
    return _by_area(records, _changing(records, COLUMNS))


def _changing(records: Sequence[LicenceRecord], columns: "tuple[str, ...]") -> "tuple[str, ...]":
    """``held`` is dropped when every row says ``yes``: the headline above already said *all*.

    A column whose value never changes is not information, it is a header over nothing -- the same
    reason the product block leaves out the twenty products that name no licence. A piped format
    keeps every field, because ``jq`` reads one record at a time and has no headline to consult.
    """
    from office365.licensing.report import YES

    if "held" in columns and {record.get("held") for record in records} == {YES}:
        return tuple(name for name in columns if name != "held")
    return columns


def _by_area(records: Sequence[LicenceRecord], columns: "tuple[str, ...]") -> str:
    """One line per licence, then the areas it opens indented under it, counts right-aligned.

    Aligned to the widest name in the whole report rather than per plan: a count column that
    moves between plans cannot be scanned down, and four plans are not worth four widths.
    """
    areas = [area for record in records for area in record["by_area"]]
    name_width = max((len(area["area"]) for area in areas), default=0)
    count_width = max((len(f"{area['nouns']:,}") for area in areas), default=1)
    sizes = {name: max((len(_cell(record, name)) for record in records), default=len(name)) for name in columns}
    lines = []
    for record in records:
        head = [_cell(record, name).ljust(sizes[name]) for name in columns[:-1]]
        nouns = record["nouns"]
        head.append(f"{nouns:,} noun" + ("" if nouns == 1 else "s"))
        lines.append("  ".join(head))
        for area in record["by_area"]:
            lines.append(f"  {area['area']:<{name_width}}  {area['nouns']:>{count_width},}")
    return "\n".join(lines)


def _cell(record: Mapping[str, object], name: str) -> str:
    """One cell of a record, read by the column's own name.

    The report's shapes are declared, but a column name arrives as a string from the format table
    above, so this is the one place the name is spent rather than a declared field.
    """
    return str(record.get(name, ""))


def _assigned(client: "GraphClient") -> "frozenset[str] | None":
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


#: What ``o365 doctor`` prints as: the page, or the whole page as one object. Not the record
#: formats, because four different shapes would have to flatten into one header row.
DOCTOR_FORMATS = ("table", "wide", "json")

#: The cells a requirement table shows: which kind of fact it is, the names it names, and what
#: this session proves of them - the licence report's own three words, so ``no`` never means
#: ``maybe``.
NEEDS_COLUMNS = ("fact", "names", "state")

#: What a requirement row says: this session proves the name, or does not. The third answer is
#: the licence report's ``unknown`` - the word it uses for a read that did not happen, which is
#: not the same as a name that is absent.
HAVE, MISSING = "have", "missing"

#: A fourth word, for the nouns whose type carries no marker at all. It is not ``have``: nothing
#: has been judged there, and counting hundreds of unstamped nouns as permissions a tenant holds
#: would be the same lie as reporting an unread fact as a missing one.
UNMARKED = "unmarked"

#: What a product page prints as: the counts, or the matrix behind them.
COVERAGE_COLUMNS = ("result", "nouns", "means")

#: The nouns that need something, grouped by what they would take: 93 rows are usually ten
#: distinct names, and the name is what a person acts on.
TAKEN_COLUMNS = ("needs", "nouns")

#: One row per noun, for ``-o wide``: the gates the type declares and what they come to. The
#: ``role`` column is added only when some noun of the product names one.
PRODUCT_NOUN_COLUMNS = ("noun", "licence", "permission", "role", "result")

#: What each format is for, in the one sentence a TAB shows beside it. One table, because
#: ``-o`` is answered by three commands and they must offer the same words with the same
#: reasons.
FORMAT_WORDS = {
    "table": "the columns a reader wants",
    "wide": "every field the payload carried",
    "json": "the payload as it came",
    "csv": "for a spreadsheet",
    "tsv": "for a spreadsheet, tab separated",
    "url": "one address per line",
    "name": "one name per line",
}


def doctor(argv: "list[str]") -> int:
    """What is configured, held and missing: this environment, or one command's requirement.

    Three questions behind one word, because all of them are asked before the first command
    runs and all are answered from declarations rather than from a call. With nothing it
    answers for the *environment*: the sessions this store keeps, what the tenant bought, the
    roles the caller holds, and how many of each product's words those plans open. With a
    product alone it answers for that product's *nouns*: which of its few hundred words this
    session can run, and which it cannot. With a route it answers for *one command*: the
    permission its declaration names, which of those names the token proves, the licence it
    needs and the roles that bypass it.

    Nothing here is sent to the service being asked about, which is the point: a refusal says
    *what happened*, this says *why*, and only one of them can be printed before the fact. A
    read that cannot be made is ``unknown`` and never ``no`` - an unread licence is not a
    missing one, and a doctor that accused a tenant of not paying for what it bought would be
    worse than a silent one.
    """
    parser = argparse.ArgumentParser(
        prog="o365 doctor",
        description="What is configured, held and missing; name a product for its nouns, a route for one command",
    )
    parser.add_argument(
        "words", nargs="*", metavar="<product> [<noun> [action]]", help="a product, or one command to ask about"
    )
    parser.add_argument("-o", "--output", choices=DOCTOR_FORMATS, default="table", help="what to print")
    args = parser.parse_args(argv)
    if len(args.words) == 1 and args.words[0] in _published():
        # A product word alone is a question about that product's nouns, never a route: the
        # router would only say that a product is not a noun. `graph` is not in the index, so
        # `o365 doctor graph` stays a route question and is refused as one.
        return _doctor_product(args.words[0], args.output)
    if args.words:
        return _doctor_route(args.words, args.output)
    return _doctor_environment(args.output)


def _doctor_environment(output: str) -> int:
    """The sessions this store holds, the tenant they speak for, and what that tenant buys.

    Three reads at most, and the product block takes none of them: it is the index alone, so a
    machine with no session still learns how many words each product opens and how many of them
    name a licence at all.
    """
    from office365.licensing.report import PRODUCT_COLUMNS, headline, of, products, rows
    from office365.runtime.render import render

    wide = output == "wide"
    document = json.loads(INDEX.read_text("utf-8"))
    declared = of(document)
    sessions = _load()
    facts = _tenant_facts()
    tenant, held, assigned, roles = facts.tenant, facts.held, facts.assigned, facts.roles
    named = rows(declared, held or (), assigned) if held is not None else []
    opened = products(document)
    if output == "json":
        print(
            json.dumps(
                {
                    "sessions": [dict(_shown(sessions[name]), audience=name) for name in sorted(sessions)],
                    "tenant": tenant,
                    "held": sorted(held or ()),
                    "roles": list(roles or ()),
                    "licences": named,
                    "products": opened,
                    "note": facts.why,
                },
                indent=2,
                default=str,
            )
        )
        return 0
    # One block per question, and exactly one blank line between them: a page assembled from
    # blocks cannot produce the double gap that printing them one at a time does.
    blocks = [_verdict(sessions, facts, named)]
    if sessions:
        blocks.append("\n\n".join(_summary(name, sessions[name], brief=True) for name in sorted(sessions)))
    if not facts.why:
        # The verdict already said what could not be read; a page that repeats it reads as two
        # problems, so only the blocks that need a tenant are printed here.
        # The areas each licence opens are names, and a name cut to fit a column is worse than
        # absent -- so the page counts them and `-o wide` prints them under the plan they belong to.
        blocks.append(
            "\n".join(
                (
                    headline(named, tenant),
                    _wrapped("roles", _roles_sentence(roles)),
                    "",
                    _licence_table(named, wide),
                )
            )
        )
    licensed = [row for row in opened if row["licensed"]]
    rest = [row for row in opened if not row["licensed"]]
    # Titled, because it answers a different question from the table above it: not what this
    # tenant holds, but which products name a licence at all -- read from the index, no session.
    coverage = ["which products name a licence", render(opened if wide else licensed, "table", columns=PRODUCT_COLUMNS)]
    if rest and not wide:
        words = sum(row["nouns"] for row in rest)
        coverage.append(
            f"no licence is named under the other {len(rest)} products ({words:,} words); -o wide lists them"
        )
    blocks.append("\n".join(coverage))
    blocks.append(
        _next(
            [
                ("o365 licences -o wide", "every licence, and the areas it opens"),
                ("o365 doctor <product> <noun> ...", "what one command needs from this session"),
            ]
        )
    )
    print("\n\n".join(block for block in blocks if block))
    return 0


def _verdict(sessions: Sessions, facts: TenantFacts, records: Sequence[Mapping[str, object]]) -> str:
    """The line a reader needs first: is anything wrong, and which command fixes it.

    A doctor that makes someone scan three blocks to find the expired token has not done its
    first job, and ``gh auth status`` and ``flutter doctor`` both lead with the answer rather
    than ending with it. Three states, and nothing else is allowed to be one: ``attention`` when
    a command would refuse right now, ``unread`` when a fact could not be read (which is not an
    accusation), and ``ok``.

    No session is ``attention`` too, because every command needs one -- but it is printed from
    the same three facts the page prints, so the line and the blocks can never disagree.
    """
    from office365.licensing.report import UNKNOWN, YES

    expired = [name for name in sorted(sessions) if _identity(name, sessions[name]).expired]
    if not sessions:
        return "doctor: attention — no session; run o365 login"
    if expired:
        which = " and ".join(expired) + (" sessions" if len(expired) > 1 else " session")
        fixes = ", ".join(f"o365 {name} login" for name in expired)
        return f"doctor: attention — the {which} expired; run {fixes}"
    if facts.why:
        return f"doctor: unread — {facts.why}"
    answers = [row["held"] for row in records]
    answered = f"{answers.count(YES)} of {len(answers)} licences" if answers else "no licence named"
    unread = answers.count(UNKNOWN)
    roles = facts.roles
    held = "roles unread" if roles is None else f"{len(roles)} role" + ("" if len(roles) == 1 else "s")
    sessions_said = f"{len(sessions)} session" + ("" if len(sessions) == 1 else "s")
    unread_said = f", {unread} unread" if unread else ""
    return f"doctor: ok — {sessions_said}, {answered}{unread_said}, {held}"


def _roles_sentence(roles: "tuple[str, ...] | None") -> str:
    """The directory roles as one line: how many, then their names, or why it is unknown.

    Eight names on a line with no count read as an unordered shrug; counted, the same names say
    what the tenant gave this identity, and the wrap keeps them on the screen.
    """
    if roles is None:
        return "unknown - the directory roles could not be read"
    if not roles:
        return "none held"
    return f"{len(roles)} held — " + ", ".join(roles)


def _doctor_route(words: "list[str]", output: str) -> int:
    """One command's declarations, marked against the session this store holds.

    The route comes from the model - one product package imported, nothing sent - and the marks
    come from the token's own ``scp``/``roles`` plus one ``subscribedSkus`` read, never from a
    call to the endpoint: the endpoint would answer with a status code, and the question is
    which *name* is missing from where.
    """
    from office365.capabilities import capabilities_of
    from office365.permissions.token import TokenClaims
    from office365.routing import route
    from office365.runtime.render import render

    speaker = " ".join(words)
    try:
        found = route(*words)
    except LookupError as error:
        return _refuse(str(error))
    if found.verb is None or found.here is None:
        answers = ", ".join(found.commands) or "-"
        return _refuse(f"{speaker} names a page, not a command; it answers: {answers}")
    declaration = capabilities_of(found.here).declarations.get(found.method)
    if declaration is None:
        # Not a refusal: the tree publishes no marker for this call, so no token could fail it.
        # Saying so is the honest answer, and an exit code would turn a gap into an error.
        print(f"o365 {speaker} declares no permission: nothing about this session decides it")
        return 0
    entry = _kept_session(_audience(found.entity))
    kept = _kept_token(entry)
    records = _needs(TokenClaims.parse(kept[0]) if kept else None, declaration)
    note = _note(kept, records)
    if output == "json":
        print(
            json.dumps(
                {"command": f"o365 {speaker}", "effect": found.verb.effect, "needs": records, "note": note}, indent=2
            )
        )
        return 0
    print(f"o365 {speaker}  ({found.verb.effect})")
    print()
    print(render(records, "table", columns=NEEDS_COLUMNS, width=None))
    if note:
        print()
        print(note)
    missing = [row["names"] for row in records if row["state"] == MISSING]
    if missing:
        print(f"needs  a session that holds: {'; '.join(missing)}")
    return 0


def _doctor_product(product: str, output: str) -> int:
    """Every noun of one product, and whether this session has what each of them declares.

    The question a page cannot answer: one product is 362 words, and "which of these can I
    actually run?" is ``doctor <route>`` asked of every noun at once. The model is read once
    and the tenant at most once, so 362 rows cost what one route costs -- nothing is sent to
    the product's own endpoints, and the marks are the same scopes, plans and roles a call
    would be judged by.

    The page counts; ``-o wide`` prints the matrix and ``-o json`` the rows. A hundred nouns
    listed one per line is a wall, and the reader's first question is a number.
    """
    from office365.routing import nouns
    from office365.runtime.render import render

    try:
        index = nouns(product)
    except LookupError as error:
        return _refuse(str(error))
    statements = sorted((_statement(found) for found in index.values()), key=lambda statement: statement.noun)
    if not statements:
        print(f"o365 doctor {product} — no noun")
        return 0
    audience = _audience(next(iter(index.values())).entity)
    # A licence or a role is the only thing that has to be asked of the tenant, and a product
    # that names neither is answered from the store alone.
    gates = _gates(audience, any(statement.plans or statement.roles for statement in statements))
    rows = [_statement_row(statement, gates) for statement in statements]
    if output == "json":
        print(json.dumps({"product": product, "nouns": rows, "note": gates.why}, indent=2, default=str))
        return 0
    if output == "wide":
        columns = [name for name in PRODUCT_NOUN_COLUMNS if name != "role" or any(row["role"] for row in rows)]
        print(render(rows, "table", columns=columns, width=None))
        return 0
    print(_coverage(product, rows, gates))
    return 0


class Statement(NamedTuple):
    """One noun's declaration, read off the model: the plans, the roles and the scopes it names."""

    noun: str
    plans: "tuple[str, ...]"
    seat: str
    roles: "tuple[str, ...]"
    declarations: "tuple[Any, ...]"


class Gates(NamedTuple):
    """What this session proves, read once for a whole product rather than once per noun."""

    claims: "TokenClaims | None"
    held: "frozenset[str] | None"
    assigned: "frozenset[str] | None"
    roles: "tuple[str, ...] | None"
    why: str


class Identity(NamedTuple):
    """What a session says about itself: who holds the token, at which site, and until when.

    Everything a greeting or a report prints is a field; the two sentences built on ``expires``
    are properties, so *how long left* and *expired how long ago* cannot disagree with the
    moment they were read from.
    """

    who: str
    tenant: str
    mode: str
    grants: str
    scopes: int
    expires: int
    site: str
    title: str

    @property
    def expired(self) -> bool:
        """Whether the token ran out: a claim with no ``exp`` is not a token that expired."""
        return bool(self.expires) and self.expires < int(time.time())

    @property
    def state(self) -> str:
        """How long the token has left, or how long since it ran out -- never the fix.

        The fact, not the fix: an expired token is said as *how long ago*, the way the live one
        is said as *how long left*. The command that renews it belongs to the doctor's verdict,
        which is the one line a reader looks for, so repeating it in a block is the same advice
        twice three lines apart.
        """
        if not self.expires:
            return ""
        now = int(time.time())
        return f"expired {_span(now - self.expires)} ago" if self.expired else f"{_span(self.expires - now)} left"


class TenantFacts(NamedTuple):
    """What the tenant says about itself, and the sentence for what it could not say."""

    tenant: str
    held: "frozenset[str] | None"
    assigned: "frozenset[str] | None"
    roles: "tuple[str, ...] | None"
    why: str


def _gates(audience: str, needed: bool) -> Gates:
    """This session's scopes, and - only when a noun names one - the tenant's plans and roles.

    ``needed`` is not an optimisation for its own sake: a product that names no licence and no
    role is answered with no request at all, and four reads to print a page they cannot change
    would make ``o365 doctor outlook`` slower than the commands it describes.
    """
    from office365.permissions.token import TokenClaims

    entry = _kept_session(audience)
    kept = _kept_token(entry)
    claims = TokenClaims.parse(kept[0]) if kept else None
    if not needed:
        return Gates(claims, frozenset(), frozenset(), (), "")
    facts = _tenant_facts()
    return Gates(claims, facts.held, facts.assigned, facts.roles, facts.why)


def _statement(found: Route) -> Statement:
    """One noun as the gates a call under it must pass.

    The licence is the type's own stamp as well as any per-call one, because a noun whose verbs
    were never stamped still names the licence its read needs -- that is the plan ``o365
    licences`` counts, and the two pages must not disagree about it.
    """
    from office365.capabilities import capabilities_of
    from office365.permissions.declaration import TENANT, licence_of

    capabilities = capabilities_of(found.entity)
    licence = licence_of(found.entity)
    declarations = tuple(capabilities.declarations.values())
    # A role is a closed vocabulary of its own, so `/directoryRoles` answers with display
    # names: the declaration holds the enum, and the value is what a name is compared to.
    roles = {getattr(role, "value", role) for declaration in declarations for role in declaration.directory_roles}
    return Statement(
        noun=found.noun,
        plans=tuple(capabilities.licenses),
        seat=licence.seat if licence is not None else TENANT,
        roles=tuple(sorted(roles)),
        declarations=declarations,
    )


def _statement_row(statement: Statement, gates: Gates) -> "dict[str, Any]":
    """One noun as a matrix row: each gate it declares, and the one word they come to."""
    permission = _permission(statement, gates)
    licence = _licence(statement, gates)
    needs = []
    if licence == MISSING:
        needs.append(f"licence {', '.join(statement.plans)}")
    if permission == MISSING:
        needs.append(f"permission {_scopes(statement)}")
    return {
        "noun": statement.noun,
        "licence": ", ".join(statement.plans),
        "permission": permission,
        "role": ", ".join(statement.roles),
        "result": _worst((licence, permission)) or UNMARKED,
        "needs": "; ".join(needs),
    }


def _licence(statement: Statement, gates: Gates) -> str:
    """Whether a plan this noun names is held, or could not be decided.

    ``answer`` is the licence report's own reading -- any one plan carries the capability -- so
    a matrix row and the ``o365 licences`` page cannot disagree about a plan name.
    """
    from office365.licensing.report import NO, UNKNOWN, YES, answer

    if not statement.plans or gates.held is None:
        return UNKNOWN if statement.plans else ""
    said = answer(statement.plans, statement.seat, gates.held, gates.assigned)
    return HAVE if said == YES else MISSING if said == NO else UNKNOWN


def _permission(statement: Statement, gates: Gates) -> str:
    """Whether this token proves what anything this noun answers asks for.

    Any one declaration satisfied is enough: a matrix row answers "is there something here I
    can do", not "may I do all of it" -- the per-verb answer is ``doctor <route>``, which
    prints each name. A role the declaration names is a bypass, so holding it decides the row
    exactly as the scope would.
    """
    from office365.licensing.report import UNKNOWN

    words = [_declared(declaration, gates) for declaration in statement.declarations]
    if not words:
        return ""
    if HAVE in words:
        return HAVE
    if any(word == UNKNOWN for word in words):
        return UNKNOWN
    return MISSING if any(words) else ""


def _declared(declaration: Any, gates: Gates) -> str:
    """One declaration against this session: ``have``, ``missing``, ``unknown``, or nothing asked.

    A marker that names only a licence or a role asks nothing of the token, and saying
    ``missing`` there would refuse a call the model never gated on a scope.
    """
    from office365.licensing.report import UNKNOWN
    from office365.permissions.requirement import FLOWS

    if any(role in (gates.roles or ()) for role in declaration.directory_roles):
        return HAVE
    flows = [(flow, getattr(declaration, flow)) for flow in FLOWS]
    if not any(names for _, names in flows):
        return ""
    if gates.claims is None:
        return UNKNOWN
    proved, silent = False, True
    for flow, names in flows:
        if not names:
            continue
        proof = gates.claims.proves(declaration.for_flow(flow))
        if proof is None:
            continue
        silent = False
        if frozenset(proof).intersection(names):
            proved = True
    if proved:
        return HAVE
    return UNKNOWN if silent else MISSING


def _worst(words: "tuple[str, ...]") -> str:
    """What a row comes to: a missing gate outranks an unread one, which outranks a held one."""
    from office365.licensing.report import UNKNOWN

    asked = [word for word in words if word]
    if MISSING in asked:
        return MISSING
    if UNKNOWN in asked:
        return UNKNOWN
    return HAVE if asked else ""


def _scopes(statement: Statement) -> str:
    """Every scope this noun's declarations name, once, for the one row that says what it lacks."""
    from office365.permissions.requirement import FLOWS

    names = {name for declaration in statement.declarations for flow in FLOWS for name in getattr(declaration, flow)}
    return ", ".join(sorted(names))


def _coverage(product: str, rows: "list[dict[str, Any]]", gates: Gates) -> str:
    """The page: how many nouns, what they come to, what the missing ones would take, what next.

    Twenty ``missing`` nouns are grouped and two hundred ``have`` nouns are counted, because a
    page is read for what is wrong with it and the wrong part is one name repeated: 41 of these
    93 wait on a single scope. ``-o wide`` is where the whole matrix belongs.
    """
    from collections import Counter

    from office365.licensing.report import UNKNOWN
    from office365.runtime.render import render

    meaning = (
        (HAVE, "this session proves what they declare"),
        (MISSING, "this session lacks what they declare"),
        (UNKNOWN, "a fact could not be read, so these are undecided"),
        (UNMARKED, "nothing is declared, so nothing here decides them"),
    )
    licensed = sum(1 for row in rows if row["licence"])
    headline = f"o365 doctor {product} — {len(rows)} nouns"
    headline += f", {licensed} name a licence" if licensed else "; none of them names a licence"
    counts = []
    for result, means in meaning:
        counted = sum(1 for row in rows if row["result"] == result)
        if counted:
            counts.append({"result": result, "nouns": counted, "means": means})
    # A prose column is never cut to a width: `nothing is declared, so nothing here decides th…`
    # says less than the same sentence in full, which is why this table asks for none.
    blocks = [headline, render(counts, "table", columns=COVERAGE_COLUMNS, width=None)]
    taken = Counter(row["needs"] for row in rows if row["result"] == MISSING)
    if taken:
        # A name that unblocks one noun is the answer to a one-noun question, and a page of
        # eighteen of them is the wall this table exists to avoid: what is worth granting is a
        # name that unblocks several, so those are printed and the rest are counted.
        grouped = sorted(taken.items(), key=_worst_first)
        worth = [{"needs": needs, "nouns": count} for needs, count in grouped if count > 1]
        alone = len(grouped) - len(worth)
        block = "what the missing ones would take"
        if worth:
            block += "\n" + render(worth, "table", columns=TAKEN_COLUMNS, width=None)
        if alone:
            block += f"\nand {alone} more name{'' if alone > 1 else 's'} one noun each; -o wide says which"
        blocks.append(block)
    if gates.why:
        # The sentence the environment page prints under its verdict, for the same reason: a
        # page that says `unknown` without saying why reads as a refusal.
        blocks.append(gates.why)
    blocks.append(
        f"next: o365 doctor {product} -o wide                     every noun, with the gates it declares\n"
        f"      o365 doctor {product} <noun> <action>             one command, name by name"
    )
    return "\n\n".join(blocks)


def _worst_first(pair: "tuple[str, int]") -> "tuple[int, str]":
    """Most nouns first, then alphabetically: the name that unblocks the most is the one to grant."""
    needs, count = pair
    return -count, needs


def _needs(claims: Any, declaration: Any) -> "list[dict[str, Any]]":
    """One record per requirement ``declaration`` states, and what this session proves of it.

    A declaration is two alternative flows and a licence, so a command that can run as a user or
    as an app prints two rows: which one applies is the session's answer, not the model's.
    """
    from office365.licensing.report import YES, answer
    from office365.permissions.declaration import USER
    from office365.permissions.requirement import FLOWS

    records = []
    for flow in FLOWS:
        names = getattr(declaration, flow)
        if names:
            proved = claims.proves(declaration.for_flow(flow)) if claims is not None else None
            records.append({"fact": flow, "names": ", ".join(names), "state": _mark(proved, names)})
    client = _live_graph() if declaration.licenses or declaration.directory_roles else None
    if declaration.licenses:
        held = _held_plans(client)
        assigned = _assigned(client) if client is not None and declaration.seat == USER else None
        proves_it = held is not None and answer(declaration.licenses, declaration.seat, held, assigned) == YES
        records.append({"fact": "licence", "names": ", ".join(declaration.licenses), "state": _word(held, proves_it)})
    if declaration.directory_roles and client is not None:
        roles = _roles(client)
        for role in declaration.directory_roles:
            records.append({"fact": "role", "names": role, "state": _mark(roles, (role,))})
    return records


def _mark(proved: "frozenset[str] | tuple[str, ...] | None", names: "tuple[str, ...]") -> str:
    """``have`` when any one of ``names`` is proved, ``missing`` when none, ``unknown`` unread.

    Any one, because the marker's own reading is a disjunction: a method that says
    ``A or B`` is satisfied by either, and that is what the guard checks too.
    """
    return _word(proved, bool(proved) and bool(frozenset(proved).intersection(names)))


def _word(asked: Any, proved: bool) -> str:
    """The row's answer: ``unknown`` when nothing was read at all, else ``have`` or ``missing``."""
    from office365.licensing.report import UNKNOWN

    if asked is None:
        return UNKNOWN
    return HAVE if proved else MISSING


def _tenant_facts() -> TenantFacts:
    """What the tenant says about itself, and the sentence for what it could not say.

    One read each: the subscriptions, the caller's own assignments, and the directory roles.
    Every failure is a sentence and an ``unknown`` rather than an exit, because a doctor that
    stopped at the first refusal would report nothing about the rest.
    """
    try:
        client = _client("graph")
    except LookupError as error:
        return TenantFacts("", None, None, None, f"the tenant could not be read: {error}")
    held = _held_plans(client)
    if held is None:
        unread = "the tenant's subscriptions could not be read: is Licence.Read.All granted?"
        return TenantFacts(client.tenant_name or "", None, None, None, unread)
    return TenantFacts(client.tenant_name or "", held, _assigned(client), _roles(client), "")


def _live_graph() -> "GraphClient | None":
    """The graph client this store can still produce, or ``None`` when it cannot."""
    try:
        return _client("graph")
    except LookupError:
        return None


def _held_plans(client: "GraphClient | None") -> "frozenset[str] | None":
    """The plans this tenant's subscriptions provision, or ``None`` when the read did not happen.

    The tenant's answer, not the caller's: which of these are assigned to a person is
    :func:`_assigned`'s question, and it is only asked when a declared seat is a person's.
    """
    from office365.runtime.client_request_exception import ClientRequestException

    if client is None:
        return None
    try:
        return client.licences.get_all().execute_query().value.plans
    except ClientRequestException:
        return None


def _roles(client: "GraphClient") -> "tuple[str, ...] | None":
    """The directory roles the calling identity holds, or ``None`` when that read cannot be made.

    ``GraphClient.require_role`` asks the same question and exits; here the answer is a row,
    because a doctor reports. An app-only session has no ``/me`` at all and a delegated one may
    lack ``RoleManagement.Read.Directory``: both are *unknown*, which is what the row says.
    """
    from office365.runtime.client_request_exception import ClientRequestException

    if client is None:
        return None
    try:
        found = client.me.get_directory_roles().execute_query()
    except (ClientRequestException, LookupError, AttributeError):
        return None
    return tuple(sorted(role.display_name for role in found if role.display_name))


def _note(kept: "tuple[str, int] | None", records: Sequence[Mapping[str, object]]) -> str:
    """The sentence under a requirement table: what the marks could not be read from."""
    from office365.licensing.report import UNKNOWN

    if kept is None:
        return "no session: run o365 login to have the token's own grants checked"
    if any(row["state"] == UNKNOWN for row in records):
        return "unknown is not missing: this token does not answer for that name, and the tenant's grant might"
    return ""


def _shown(entry: Session) -> "dict[str, object]":
    """A session as a report may print it: everything but the two fields that hold secrets."""
    return {name: value for name, value in entry.items() if name not in ("token", "cache")}


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
    if words[0] == "config":
        return _prefixed([(setting.key, setting.spoken) for setting in SETTINGS], prefix)
    if words[0] in ("doctor", "licences") and words[-1:] in (["-o"], ["--output"]):
        return _prefixed(_format_words(DOCTOR_FORMATS if words[0] == "doctor" else LICENCE_FORMATS), prefix)
    if words[0] == "licences":
        return []
    if words[0] == "doctor":
        # The page takes the same route as the command it describes, so it answers with the same
        # words: a product before a noun, then whatever the route reached.
        return _prefixed(_products() if len(words) == 1 else _after(words[1], words[2:]), prefix)
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
    """Nothing typed yet: what owns a token, what owns types, and the words that own neither."""
    return (
        [(name, "audience") for name in AUDIENCES]
        + _products()
        + _sessions()
        + [
            ("config", "what a login reads, and where"),
            ("completion", "shell script"),
            ("licences", "what this tenant holds"),
            ("doctor", "what this session can do"),
            ("help", "any of these pages"),
        ]
    )


def _products() -> "list[tuple[str, str]]":
    """The products a token answers, minus the ones that are audiences and so already offered."""
    return [(name, "product") for name in _published() if name not in AUDIENCES]


def _sessions() -> "list[tuple[str, str]]":
    """The verbs that speak to the session rather than to the service."""
    return [(name, "session") for name in SESSION]


def _flag_words(found: Route) -> "list[tuple[str, str]]":
    """The flags a command takes: its own parameters, then what every command prints with."""
    method = getattr(found.reached, found.method)
    answer = []
    for name, parameter in _signature(method).parameters.items():
        if name in SUPPLIED or parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            continue
        answer.append(("--" + name.replace("_", "-"), getattr(_unoptional(parameter.annotation), "__name__", "")))
    return (
        answer
        + ([("--id", "the key of the item this command acts on")] if _keyed(found, method) else [])
        + [
            ("-o", "the format to print"),
            ("--output", "the format to print"),
            ("--columns", "the names the table shows"),
            ("--no-headers", "rows without the header line"),
            ("--link", "when a name carries its URL"),
        ]
        + ([("--yes", "send a destroy action without asking")] if found.verb and found.verb.confirm else [])
        + [
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

        return _format_words(FORMATS)
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


def _format_words(choices: "tuple[str, ...]") -> "list[tuple[str, str]]":
    """The values ``-o`` takes for one command. A command offers only the formats it accepts:
    a TAB that answers ``csv`` for ``doctor`` would hand back a word argparse refuses.
    """
    return [(choice, FORMAT_WORDS.get(choice, "")) for choice in choices]


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
    if not words or words[:1] in (["-h"], ["--help"]):
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
    from office365.routing import route

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
    root = _root(_audience(found.entity))
    walk = _walk(root, found)
    keyed = _keyed(found, method)
    address = _feed(root, found, product) if keyed else None
    tail = found.walk if found.listing else ()
    parser = argparse.ArgumentParser(
        prog=f"o365 {product} {spoken}",
        description=_reaches(found, target, walk, address, tail),
        epilog="\n".join(_hints(target, found.method)),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    from office365.runtime.render import FORMATS

    _flags(parser, method, {"id"} if keyed else set())
    if keyed:
        parser.add_argument(
            "--id",
            default=None,
            metavar="<key>",
            help="address the item this key names, by id or by its alternate key",
        )
    parser.add_argument("-o", "--output", choices=FORMATS, default="table", help="what to print")
    parser.add_argument("--columns", default=None, help="comma separated names the table shows")
    parser.add_argument("--no-headers", action="store_true", help="print rows without the header line")
    parser.add_argument(
        "--link", choices=("auto", "always", "never"), default="auto", help="when a name carries its URL"
    )
    if "base_url" in _signature(root).parameters:
        parser.add_argument(
            "-s",
            "--site",
            default=os.environ.get("O365_SITE") or None,
            help="address another site for this command only (default: $O365_SITE)",
        )
    if found.verb.confirm:
        parser.add_argument("-y", "--yes", action="store_true", help="send a destroy action without asking")
    parser.add_argument("-n", "--dry-run", action="store_true", help="print the request and send nothing")
    args = parser.parse_args(argv)
    given = _accepted(args, method)
    # A destroy action is the one that asks, and `confirm` is derived from the effect, so this
    # gate cannot drift from the effect the page printed. It sits before the session is read:
    # "may I?" is answerable with no token, and a refusal costs no request.
    if found.verb.confirm and not (getattr(args, "yes", False) or args.dry_run):
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
    noun = found.walk[-1] if found.walk else found.noun
    if getattr(args, "id", None):
        # A key is what the walk could not invent: 3601 routes end on an item whose feed is an
        # argument to the getter, so `--id` supplies it and the rest of the walk is unchanged.
        if address is None:
            return _refuse(f"{product} {spoken} names no feed for --id to address")
        feed = functools.reduce(getattr, address, client)
        method = getattr(functools.reduce(getattr, tail, feed[args.id]), found.method)
    elif walk is None:
        # The hint is offered only where it would work: a route whose noun states no feed has no
        # key to take, and pointing it at `--id` would be the refusal promising a flag it lacks.
        return _refuse(
            f"{product} {spoken} is declared, but nothing walks there from {type(client).__name__}:"
            " every link on the way needs an argument the model does not name yet"
            + ("; --id names it" if address is not None else "")
        )
    else:
        method = getattr(functools.reduce(getattr, walk, client), found.method)
    return _send(client, method, given, args, found.shows, empty=f"No {noun} found.")


def _keyed(found: Route, method: Callable[..., Any]) -> bool:
    """Whether ``--id`` names the item this command acts on.

    ``list`` reads a feed that hangs off an item (a message's attachments) and every other verb
    acts on the item itself, so both are addressed by the key of that item. A verb declared on
    the feed -- ``create`` -- has no item to name, a noun that states no feed has nowhere to put
    one, and a method that already takes an ``id`` is addressed by its own flag rather than by a
    second spelling of it.
    """
    from office365.runtime.client_object_collection import ClientObjectCollection

    if found.collection is None or "id" in _signature(method).parameters:
        return False
    if found.listing:
        return bool(found.walk)
    return not issubclass(found.reached, ClientObjectCollection)


def _feed(root: type, found: Route, product: str) -> "tuple[str, ...] | None":
    """The attributes to walk to the feed whose item ``--id`` names.

    A listing's item is the one the noun names -- ``message attachments list`` addresses a
    message, then reads its attachments -- while every other verb lands on the item the words
    reached, so the feed is the one that holds *that* type (``web lists delete`` addresses a
    list). Both are read off the model: the noun's own route for the first, the last step for
    the second.
    """
    from office365.entity_collection import EntityCollection
    from office365.routing import chain, route
    from office365.runtime.client_object_collection import ClientObjectCollection

    held = route(product, found.noun).collection if found.listing else found.collection
    if held is None or held in (ClientObjectCollection, EntityCollection):
        # A link typed `EntityCollection[X]` holds the base class at run time, so walking to it
        # would index whichever feed the walk reached first. A URL nobody asked for is worse
        # than no URL, and the noun's own feed names the type or says nothing.
        return None
    return chain(root, held)


def _reaches(
    found: Route,
    target: type,
    walk: "tuple[str, ...] | None",
    address: "tuple[str, ...] | None",
    tail: "tuple[str, ...]",
) -> str:
    """What ``-h`` says the command reaches, in the order it gets there.

    A route ``--id`` completes walks to the feed and indexes it, so the key is shown where it is
    used -- ``users[<id>]`` -- instead of the item the model happens to reach first (``me``).
    """
    if address:
        walked = " -> ".join([*address[:-1], f"{address[-1]}[<id>]", *tail])
    elif walk:
        walked = " -> ".join(walk)
    else:
        return f"{found.method}() on {target.__name__}"
    return f"Walk {walked}, then {found.method}() on {target.__name__}"


def _walk(root: type, found: Route) -> "tuple[str, ...] | None":
    """The attributes to walk from the root to the object that holds the method.

    A ``list`` is ``get()`` on the feed, so it has to reach the feed and not one item of it:
    ``chain(root, Message)`` is ``None`` while ``chain(root, MessageCollection)`` is
    ``me.messages``, and taking the entity there asked ``/me`` for a list of users. The item is
    the target for every other verb, followed by the navigation the route already recorded
    (``attachments`` for a message's feed, which is the one that cannot be walked to from the
    root at all - a message has to be addressed by id, and the model does not name one).
    """
    from office365.routing import chain

    if found.listing and isinstance(found.here, type):
        # A listing's target is the feed the words reached, not one item of it
        # (`chain(root, Message)` is ``None`` where ``chain(root, MessageCollection)`` is
        # ``me.messages``); the walk is ``get()`` on that feed.
        return chain(root, found.here)
    path = chain(root, found.entity)
    return None if path is None else path + found.walk


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


def _page(product: str, spoken: str, found: Route) -> str:
    """The page a node answers: what it is, what it answers, what it holds, what to type next.

    Every line is read off the model: the actions are the type's stamped verbs, the groups are
    the effect each declares, the links are the getters the walk accepts, and the columns a
    read shows are the type's ranked defaults (``-o wide`` shows every field the payload
    carried). So nothing here is a vocabulary someone has to keep in step with the library.
    """
    from office365.permissions.declaration import TENANT, licence_of
    from office365.routing import navigations
    from office365.runtime.schema import TypeSchema

    here = found.reached
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


def _examples(product: str, spoken: str, found: Route, links: "list[str]") -> "list[str]":
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
    client: "ClientRuntimeContext",
    method: Callable[..., Any],
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


def _preview(client: "ClientRuntimeContext") -> str:
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


def _can_select(result: object) -> bool:
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


def render_origin(client: "ClientRuntimeContext") -> str:
    """``scheme://host`` for the server-relative links a SharePoint payload carries."""
    from office365.runtime.render import origin_of

    return origin_of(getattr(client, "service_root_url", None))


def _addresses(rows: Sequence[object]) -> "list[str | None]":
    """Each row's own REST address -- one per row, so it lines up with the record it belongs to."""
    return [None if isinstance(row, Mapping) else getattr(row, "resource_url", None) for row in rows]


def _payload(row: object) -> "Mapping[str, Any]":
    """One row as what a table reads: the object's own JSON, or a value under ``value``."""
    to_json = getattr(row, "to_json", None)
    payload = to_json() if callable(to_json) else row
    return payload if isinstance(payload, Mapping) else {"value": payload}


def _columns(records: Sequence["Mapping[str, Any]"], chosen: "str | None", entity: type) -> "list[str] | None":
    """The columns a table shows: the ones asked for, or the ones the type says a reader wants."""
    if chosen:
        return [name.strip() for name in chosen.split(",") if name.strip()]
    from office365.runtime.schema import TypeSchema

    spelled = {name.lower(): name for name in sorted({name for r in records if isinstance(r, Mapping) for name in r})}
    wanted = TypeSchema.of(entity).defaults
    return [spelled[name.lower()] for name in wanted if name.lower() in spelled] or None


def _rows(result: object) -> "list[object]":
    """What a command prints, one entry per row: a collection's items, or the one object.

    The items and not their JSON, because a row needs both halves: the payload the table
    reads and the REST address the row links to. ``to_json()`` on a collection has only the
    first, which is how a table of 146 lists came out with no addresses.
    """
    from office365.runtime.client_object import ClientObject
    from office365.runtime.client_object_collection import ClientObjectCollection
    from office365.runtime.client_value import ClientValue

    if isinstance(result, (list, tuple)):
        return list(result)
    if isinstance(result, Mapping):
        return [result]
    if isinstance(result, ClientObjectCollection):
        # Only a collection is a feed. An entity iterates its own fields as ``(name, value,
        # stated)`` triples -- that is what a request carries -- so iterating a ``Web`` would
        # print one row per field: `["Title", "SiteU74H3Z9O", false]` under a `VALUE` heading.
        # An empty feed is no rows, not the feed as one row: the caller's sentence (`No device
        # found.`) is the answer, and the old fallback printed the envelope -- `value  []`.
        return list(result)
    if isinstance(result, (ClientObject, ClientValue)):
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
    constructor: dict[str, object] = dict(entry.get("constructor") or {})
    if "base_url" in constructor:
        # The site is the boundary: this command addresses one site collection, and `use` or
        # `--site` says which. What login was given is the answer until one is chosen.
        wanted = site or _current(entry)
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


def _token(entry: Session) -> str:
    """The access token the session still holds; nothing here refreshes it."""
    kept = _kept_token(entry)
    if kept is None or kept[1] <= time.time():
        raise LookupError(f"the {entry.get('mode', '')} session has no live token here; run login again")
    return kept[0]


def _kept_token(entry: Session) -> "tuple[str, int] | None":
    """The freshest token the session kept - expired or not - and when it expires.

    ``_token`` refuses an expired one because a request would fail; a report does not, it says
    how old its facts are. Two questions about one store, so one place reads it: the token
    itself, and MSAL's cache beside it, which is where a renewed one lands. That cache is MSAL's
    own document, so its shape is read as ``Any`` and answered as the pair this returns.
    """
    kept = entry.get("token") or {}
    candidates: "list[tuple[str, int]]" = []
    if kept.get("access_token"):
        candidates.append((str(kept.get("access_token")), kept.get("expires_on", 0)))
    cache: dict[str, Any] = json.loads(entry.get("cache") or "{}")
    for token in cache.get("AccessToken", {}).values():
        if token.get("secret"):
            candidates.append((str(token["secret"]), int(token.get("expires_on", 0))))
    return max(candidates, key=lambda held: held[1]) if candidates else None


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


def _setting(name: str) -> Setting:
    """The setting named ``name``: its key, the word a sentence uses, and its two shortcuts."""
    return next(setting for setting in SETTINGS if setting.key == name)


def _short_path(path: Path) -> str:
    """The file as a person spells it -- ``~/.o365/config.json`` -- and the full path elsewhere.

    A report that says *where* a value came from is only useful if it names a path you can open,
    and the home directory is the one prefix a reader already knows.
    """
    spelled = str(path)
    home = str(Path.home())
    return "~" + spelled[len(home) :] if spelled.startswith(home) else spelled


def _resolved(name: str, kept: "Mapping[str, str]") -> "tuple[str, str]":
    """One setting's effective value and where it came from.

    The order is the one a login applies -- this shell, then the file, then the tenant's own
    default -- so ``o365 config tenant`` answers with exactly what a command would use. A flag is
    the fourth answer and cannot show here: it belongs to the run that carried it.
    """
    setting = _setting(name)
    given = os.environ.get(setting.env, "")
    if given:
        return given, "environment"
    if kept.get(name):
        return str(kept[name]), _short_path(_config())
    if name == "site":
        # The host a `<label>.onmicrosoft.com` tenant gets by default. A login still checks it
        # with one read before addressing a session at it; this report sends no request at all.
        derived = _derived_site(os.environ.get("O365_TENANT", "") or str(kept.get("tenant", "")))
        if derived:
            return derived, "derived from the tenant"
    return "", "not set"


def _advice(missing: "list[str]") -> str:
    """How to answer a setting this run needs, as a block a person can paste and be done.

    The snippet is the file *as it would be*, not a template of it: a value already kept is
    repeated, because ``cat >`` replaces the whole document and answering one question must not
    cost another. The path is this machine's, so not a word of it needs editing.
    """
    kept = _prefs()
    # Only what is answered, plus what was asked for: an empty key in the snippet would answer
    # nothing and read as though it had been filled in.
    document = {setting.key: str(kept[setting.key]) for setting in SETTINGS if kept.get(setting.key)}
    for name in missing:
        document[name] = EXAMPLES[name]
    path = _config()
    spoken = " or ".join(_setting(name).spoken for name in missing)
    body = "\n".join("    " + line for line in json.dumps(document, indent=2).splitlines())
    envs = " ".join(f"{_setting(name).env}=<{_setting(name).spoken.replace(' ', '-')}>" for name in missing)
    flags = " ".join(f"{_setting(name).flag} <{_setting(name).spoken.replace(' ', '-')}>" for name in missing)
    return (
        f"no {spoken} yet\n\n"
        "  Give it once, so that no command has to repeat it\n"
        f"  (a file you own: o365 config reads it, and never writes to it):\n\n"
        f"    mkdir -p {_short_path(path.parent)}\n"
        f"    cat > {_short_path(path)} <<'EOF'\n"
        f"{body}\n"
        "    EOF\n\n"
        f"  or for this shell:  export {envs}\n"
        f"  or for one command: {flags}\n"
        "  o365 config says what is answered already, and where each answer came from"
    )


def config(argv: "list[str]") -> int:
    """What this machine answers, where each answer came from, and how to answer the rest.

    Read only by design: a preference is not a secret, so it lives in a file the person owns and
    this command has no business rewriting it. Saying the chain is the useful half -- the shape
    ``aws configure list`` has -- and ``o365 config <key>`` prints one resolved value, so a script
    reads what a command would use instead of restating the precedence.
    """
    parser = argparse.ArgumentParser(
        prog="o365 config",
        description="The settings a login reads once: what is answered, from where, and the file to edit.",
    )
    parser.add_argument(
        "key",
        nargs="?",
        choices=[setting.key for setting in SETTINGS],
        help="print this setting's resolved value, and exit 1 when nothing answers it",
    )
    args = parser.parse_args(argv)
    kept = _prefs()
    if args.key:
        value = _resolved(args.key, kept)[0]
        if not value:
            print(_advice([args.key]), file=sys.stderr)
            return 1
        print(value)
        return 0

    from office365.runtime.render import render

    rows = []
    for setting in SETTINGS:
        value, origin = _resolved(setting.key, kept)
        rows.append({"setting": setting.key, "value": value or NOT_SET, "from": origin})
    print(render(rows, "table", columns=("setting", "value", "from")))
    print()
    print(f"file         {_short_path(_config())}   (read only: edit it yourself)")
    print("flags        --tenant, --client-id, --base-url   (one run, and they win)")
    print("environment  O365_TENANT, O365_CLIENT_ID, O365_SITE")
    if not _resolved("client_id", kept)[0]:
        # A login cannot start without one, so this is the one row worth spelling out in full.
        print()
        print(_advice(["client_id"]))
    return 0


def _load() -> Sessions:
    """Every kept session, or nothing when there is no readable store."""
    try:
        return json.loads(_store().read_text("utf-8"))
    except (OSError, ValueError):
        return {}


def _kept_session(audience: str) -> Session:
    """The session this audience keeps, or an empty one when nothing is stored."""
    return _load().get(audience) or Session()


def _save(sessions: Sessions) -> None:
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


def _identity(audience: str, entry: Session) -> Identity:
    """What a kept session says about itself, decoded from the token it holds.

    One decode for the three answers built on it: ``whoami`` names the grants, a login counts
    them, and ``doctor`` counts them from one row. Nothing here sends a request -- a claim is
    already in the file the session was saved to.

    The claims are a decoded JWT, so the payload's shape is the token's and not this library's:
    each is read once, here, and answered as text, which is what makes the rest of this file
    typed. ``exp`` is the one that has to stay a number.
    """
    claims: dict[str, Any] = entry.get("claims") or {}
    grants = str(claims.get("scp") or " ".join(claims.get("roles") or []) or "-")
    site = _current(entry)
    return Identity(
        who=str(claims.get("preferred_username") or claims.get("upn") or claims.get("appid") or "<unknown>"),
        tenant=str(claims.get("tid") or "-"),
        mode=entry.get("mode", ""),
        grants=grants,
        scopes=0 if grants == "-" else len(grants.split()),
        expires=int(claims.get("exp") or 0),
        site=site,
        title=next((held.get("title", "") for held in entry.get("contexts", []) if _url_of(held) == site), ""),
    )


def _span(seconds: int) -> str:
    """A duration as a person says it: ``59 min``, ``2 h``, ``3 d``.

    A token lives an hour, so minutes are the unit a reader is looking at; a session left alone
    for a week is not ``10080 min``.
    """
    hour, day = 60, 60 * 24
    minutes = max(0, seconds) // 60
    if minutes < hour:
        return f"{minutes} min"
    if minutes < day:
        return f"{minutes // hour} h"
    return f"{minutes // day} d"


def _wrapped(label: str, text: str) -> str:
    """``label: text`` wrapped to the terminal, hanging under the first word after the label.

    Fifty-five scope names are one unreadable line; wrapped, the same list is scannable, and the
    wrap is the terminal's own width rather than a number this file guesses at.
    """
    width = min(100, max(40, shutil.get_terminal_size((100, 24)).columns))
    indent = " " * (len(label) + 2)
    return textwrap.fill(text, width=width, initial_indent=f"  {label}: ", subsequent_indent=indent + "  ")


def _summary(audience: str, entry: Session, brief: bool = False) -> str:
    """One line of who the session is, and whether it still holds.

    ``brief`` counts the token's grants instead of naming them: a doctor page asks what the
    tenant has, and seventy scope names would push that off the screen. ``whoami`` is the word
    that lists them.
    """
    facts = _identity(audience, entry)
    grants = facts.grants
    if brief and facts.scopes:
        grants = f"{facts.scopes} scope" + ("s" if facts.scopes != 1 else "")
    aside = f", {facts.state}" if facts.state else ""
    where = f"(tenant {facts.tenant}, mode {facts.mode}{aside})"
    line = f"{audience}: {facts.who} {where}\n{_wrapped('grants', grants)}"
    if facts.site:
        line += f"\n  at {_short(facts.site)}" + (f" — {facts.title}" if facts.title else "")
    return line


def _welcome(audience: str, entry: Session) -> str:
    """What a login says: that you are in, for how long, and the two words that answer the rest.

    A login is a greeting, not a report. Seventeen lines of scope names are unreadable at the
    moment a person is trying to start work, and printing them buried the only three facts that
    matter here -- which audience, who, how long. The grants are the answer to a question nobody
    has asked yet: ``o365 whoami`` names them, and ``o365 doctor`` says what the tenant allows.
    """
    facts = _identity(audience, entry)
    held = f"{facts.scopes} permission" + ("" if facts.scopes == 1 else "s") if facts.scopes else "no permissions"
    facts_line = ", ".join(part for part in (facts.mode, held, facts.state) if part)
    line = f"logged in: {audience} as {facts.who} ({facts_line})"
    if facts.site:
        line += f"\n  at {_short(facts.site)}" + (f" — {facts.title}" if facts.title else "")
    line += "\n  o365 whoami names the grants; o365 doctor says what this tenant allows"
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
        "       o365 config [<key>]                (what is set, and the file to edit)\n"
        "       o365 completion bash|zsh|fish [--warm [product ...]]\n"
        "       o365 licences [-o table|wide|csv|tsv|json]\n"
        "       o365 doctor [<product> [<noun> [action]]] [-o table|wide|json]\n"
        "  a flag falls back to O365_CLIENT_ID/O365_TENANT/O365_SITE, then to ~/.o365/config.json"
    )


def _plain(value: object) -> object:
    """A constructor argument as JSON can keep it."""
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return [_plain(item) for item in value]
    return value


if __name__ == "__main__":
    raise SystemExit(main())
