"""A command line that reads the declarations instead of restating them.

Grammar, ``az``-shaped and with the audience first because a token belongs to one::

    o365 login [--audience graph|sharepoint|exchange] [--mode device-flow] \\
               --tenant contoso.onmicrosoft.com --client-id <id> [--scopes User.Read Mail.Read]
    o365 whoami [--audience ...]
    o365 logout [--audience ...]
    o365 <product> <noun> <action> [flags]

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
"""

from __future__ import annotations

import argparse
import base64
import functools
import importlib
import inspect
import json
import os
import sys
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


def main(argv: "list[str] | None" = None) -> int:
    """Run one command, returning the process exit code."""
    words = list(sys.argv[1:] if argv is None else argv)
    # An audience word names a session, so it is only taken when a session verb follows it:
    # `o365 sharepoint login` is the sharepoint session, `o365 sharepoint web get` the product.
    audience = words.pop(0) if len(words) > 1 and words[1] in SESSION and words[0] in AUDIENCES else ""
    if not words or words[0] in ("-h", "--help"):
        print(_usage())
        return 0 if words else 2
    word, rest = words[0], words[1:]
    if word == "login":
        return login(audience or "graph", rest)
    if word == "whoami":
        return whoami(audience)
    if word == "logout":
        return logout(audience)
    if not rest:
        print(f"o365: unknown command {word!r}\n{_usage()}", file=sys.stderr)
        return 2
    noun, rest = rest[0], rest[1:]
    # The words name the route and stop where the first flag starts; a flag's value is not a word.
    cut = next((position for position, item in enumerate(rest) if item.startswith("-")), len(rest))
    return command(word, [noun, *rest[:cut]], rest[cut:])


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
        print(f"{product} {spoken}: " + ", ".join(sorted(found.commands)))
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
    _flags(parser, method, set())
    given = _accepted(parser.parse_args(argv), method)

    try:
        client = _client(_audience(found.entity))
    except LookupError as err:
        return _refuse(str(err))
    if walk is None:
        return _refuse(
            f"{product} {spoken} is declared, but nothing walks there from {type(client).__name__}:"
            " every link on the way needs an argument the model does not name yet"
        )
    return _send(client, getattr(functools.reduce(getattr, walk, client), found.method), given)


def _send(client: Any, method: Any, given: "Mapping[str, Any]") -> int:
    """Call the method, run the one query it queued, and print what came back."""
    from office365.runtime.client_request_exception import ClientRequestException

    result = method(**given)
    try:
        client.execute_query()
    except ClientRequestException as err:
        return _refuse(str(err), 1)
    print(json.dumps(_rows(result), indent=2, default=str))
    return 0


def _rows(result: Any) -> Any:
    """What a command prints: the payload the object serializes to, always as a list."""
    payload = result.to_json() if hasattr(result, "to_json") else result
    return payload if isinstance(payload, list) else [payload]


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
    """The three words this command line knows today."""
    return (
        "usage: o365 [graph|sharepoint|exchange] login|whoami|logout [flags]\n"
        "       o365 login --tenant <tenant> --client-id <id> [--mode device-flow] [--scopes ...]"
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
