"""A command line that reads the declarations instead of restating them.

Grammar, ``az``-shaped and with the audience first because a token belongs to one::

    o365 login [--audience graph|sharepoint|exchange] [--mode device-flow] \\
               --tenant contoso.onmicrosoft.com --client-id <id> [--scopes User.Read Mail.Read]
    o365 whoami [--audience ...]
    o365 logout [--audience ...]
    o365 <product> <noun> [navigation ...] [action] [-o table|wide|json|csv|tsv|url|name] [flags]
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

Two things the command line supplies rather than accepts: the ``token_cache`` (the
session file *is* the cache) and ``client_id``, which is mandatory - this library ships
no app registration of its own, so ``--client-id`` or ``O365_CLIENT_ID`` is required.
A ``--password`` is a flag like any other, which also means it is visible in the process
list; a secret store behind ``--authority``/``--client-secret`` is the better habit.

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
    if word == "login":
        return login(audience or "graph", rest)
    if word == "whoami":
        return whoami(audience)
    if word == "logout":
        return logout(audience)
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
    given["client_id"] = given.get("client_id") or os.environ.get("O365_CLIENT_ID", "")
    if not given["client_id"]:
        parser.error("--client-id (or O365_CLIENT_ID) is required: this library ships no app registration of its own")

    import msal

    # The session file *is* the cache, so it is handed in rather than accepted as a flag.
    cache = msal.SerializableTokenCache() if "token_cache" in inspect.signature(root).parameters else None
    if cache is not None:
        given["token_cache"] = cache

    constructor = {name: value for name, value in given.items() if name in inspect.signature(root).parameters}
    client = root(**constructor)
    getattr(client, method)(**{name: value for name, value in given.items() if name not in constructor})
    # Both providers state the same property: acquired on first read, cached, never validated.
    token = client.pending_request().authentication_context.access_token or ""
    claims = _claims(token)

    sessions = _load()
    sessions[audience] = {
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


def _refuse(message: str, code: int = 2) -> int:
    """Say why nothing ran, and answer the shell with a non-zero code."""
    print(f"o365: {message}", file=sys.stderr)
    return code


def _audience_words(words: "list[str]") -> tuple[str, "list[str]"]:
    """Take a leading audience word off the line, and say which session the line is about.

    An audience word is taken in two cases: a session verb follows it, so ``o365 sharepoint
    login`` is the sharepoint session and not the sharepoint product; or the tree has no package
    of that name, which is ``graph`` alone, so ``o365 graph directory user get`` is the directory
    user and ``o365 graph`` asks what that one token serves. ``o365 sharepoint web get`` keeps its
    word, because there is a package behind it.
    """
    if not words or words[0] not in AUDIENCES:
        return "", words
    if len(words) > 1 and words[1] in SESSION:
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
    offered = _after(head, rest)
    if not rest and head in AUDIENCES:
        offered += _sessions()
    return _prefixed(offered, prefix)


def _after(product: str, path: "list[str]") -> "list[tuple[str, str]]":
    """What may follow ``<product> <path>``: nouns, a route's words, or a command's flags."""
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
        + [("completion", "shell script"), ("help", "any of these pages")]
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
    return answer + [
        ("-o", "the format to print"),
        ("--output", "the format to print"),
        ("--columns", "the names the table shows"),
        ("--no-headers", "rows without the header line"),
        ("--link", "when a name carries its URL"),
    ]


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
    )
    from office365.runtime.render import FORMATS

    _flags(parser, method, set())
    parser.add_argument("-o", "--output", choices=FORMATS, default="table", help="what to print")
    parser.add_argument("--columns", default=None, help="comma separated names the table shows")
    parser.add_argument("--no-headers", action="store_true", help="print rows without the header line")
    parser.add_argument(
        "--link", choices=("auto", "always", "never"), default="auto", help="when a name carries its URL"
    )
    args = parser.parse_args(argv)
    given = _accepted(args, method)

    try:
        client = _client(_audience(found.entity))
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
        found.entity,
        empty=f"No {noun} found.",
    )


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
    from office365.routing import navigations
    from office365.runtime.schema import TypeSchema

    here = found.here or found.entity
    schema = TypeSchema.of(here)
    lines = [f"{product} {spoken} \u2014 {here.__name__}"]
    if schema.defaults:
        lines.append(f"  a read shows {', '.join(schema.defaults)}")
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
        columns = TypeSchema.of(found.here or found.entity).defaults
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
    try:
        client.execute_query()
    except ClientRequestException as err:
        return _refuse(str(err), 1)
    rows = _rows(result)
    records = [_payload(row) for row in rows]
    print(
        render(
            records,
            args.output,
            columns=_columns(records, args.columns, entity),
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
    if hasattr(result, "__iter__") and hasattr(result, "to_json"):
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


def _client(audience: str) -> Any:
    """A client for ``audience``, holding the token its session kept.

    A command does not log in: it either finds a live token in the store or says to run
    ``login`` again. Re-running the mode would need the credentials a session must not
    keep - the second half of ``username-and-password`` was missing on the first live run.
    """
    entry = _load().get(audience)
    if entry is None:
        ran = "o365 login" if audience == "graph" else f"o365 {audience} login"
        raise LookupError(f"no session for {audience}; run {ran}")
    client = _root(audience)(**dict(entry["constructor"]))
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
    state = " (expired; run o365 login)" if expires and expires < time.time() else left
    return f"{audience}: {who} (tenant {claims.get('tid', '-')}, mode {entry['mode']}{state})\n  grants: {grants}"


def _usage() -> str:
    """What this command line knows: a session, a route of words, and the shell script."""
    return (
        "usage: o365 [graph|sharepoint|exchange] login|whoami|logout [flags]\n"
        "       o365 <product> <noun> [navigation ...] [action] [flags]\n"
        "       o365 <product> <noun> list [-o table|wide|json|csv|tsv|url|name]\n"
        "       o365 graph <product> <noun> [navigation ...] [action]\n"
        "       o365 login --tenant <tenant> --client-id <id> [--mode device-flow] [--scopes ...]\n"
        "       o365 completion bash|zsh|fish [--warm [product ...]]"
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
