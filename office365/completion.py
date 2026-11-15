"""The words that may follow, read off the model and kept in a cache.

A shell asks for the word under the cursor on every TAB, in a process of its own, so the
answer has to be cheap twice: cheap to compute once, cheap to read afterwards. What is
expensive here is *importing a product* -- ``sharepoint`` is 2 567 modules and 0.9 s before
its first noun is known -- and nothing else, because the words that follow a noun are two
declarations the model already states: the commands of a route and the links the walk holds
(:func:`office365.routing.navigations`), both ``@cache``d per class.

So the answers are written down per product - every noun, and every link it holds, so that a
TAB one level deeper does not pay an import either - and validated with the mtimes of exactly
the modules that produced them: an edit anywhere under the product rebuilds that product's
answers instead of serving a word the library no longer has. Measured here: the whole tree is
8 168 nodes over 6 947 modules in 3.2 MB, 5.7 s to fill once; reading it back costs 34 ms and
validating one product 0.9 ms, which is what a TAB pays instead of a 0.1-1.5 s import.

Three rules keep the cache honest, the same three the shipped index follows: it is written
by this module and never by hand; it may be *wrong*, never *stale* (a node whose stamp does
not match is recomputed, a file that does not parse is ignored); it is a cache, not a model,
so deleting it costs one import and nothing else.

A word is offered only when the router would accept it: a noun is what ``nouns()``
publishes, a link is what ``navigations()`` returns, and an action is what ``@verb`` stamps
``expose=True``. A command line that completes a word it cannot walk advertises a URL it
cannot build, so the completer and :func:`office365.routing.route` read one answer.

The three shell scripts are here rather than in the command line because they are the other
half of the same protocol: a hidden ``__complete`` that speaks words, and a function that
asks it. ``bash`` keeps only the words (``compgen`` has nowhere to put a description),
``zsh`` asks for them without one, and ``fish`` reads ``word<TAB>description`` natively,
which is why the protocol carries the description at all.

One shape of answer is not a word: a line that ends on an action. That node is cached too, as
``None``, because saying where the walk stopped is the cheap half of the answer - but the
flags that follow are the method's signature, so the caller reads them off the method and
that one TAB pays the product's import.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple

#: The cache layout, bumped when an older file would be read as this one.
FORMAT = 1

#: Where the cache is written when ``XDG_CACHE_HOME`` and ``O365_CACHE`` say nothing.
DEFAULT_CACHE = "~/.cache/o365/completion.json"

#: The shells this module can speak to, by the word a user types after ``completion``.
SHELLS = ("bash", "zsh", "fish")


@dataclass(frozen=True)
class Candidate:
    """One word a shell may offer, and what the line would reach by taking it.

    :attr:`kind` is the class of word - ``noun``, ``navigation`` or ``action`` - and
    :attr:`detail` is the same fact with its landing spelled out: the type a noun or a link
    holds, or the effect of an action (``read``, ``write``, ``destroy``), which is what a
    reader wants before choosing one. A shell that shows no description keeps the word.
    """

    word: str
    kind: str
    detail: str = ""

    def line(self) -> str:
        return f"{self.word}\t{self.detail or self.kind}"


def following(product: str, path: "Sequence[str]" = ()) -> "Optional[Tuple[Candidate, ...]]":
    """The words that may follow ``<product> <path>``, in the order a shell should show them.

    An empty ``path`` answers the product's nouns; a path that names a noun answers what that
    type answers and holds, actions first. ``None`` is the third answer, and it is not a
    failure: the path ends on an action, so what follows is that command's flags and values,
    which are its signature rather than a word of the model. The caller reads those itself,
    off the method, and this module says only that the walk stopped.
    """
    document = _document()
    key = " ".join((product, *path))
    if _fresh(document["stamps"].get(product)) and key in document["nodes"]:
        return _thaw(document["nodes"][key])
    built = _build(product, path)
    _remember(document, product, key, built)
    return built


def warm(products: "Iterable[str]", out: "Callable[[str], Any]" = print) -> int:
    """Fill the cache for every word of ``products``, so no TAB pays the import.

    The walk is the same one the shipped index makes - each product's package imported once,
    then every noun and every link it holds followed - but each type is expanded once, so a
    graph with many roads to the same folder costs one import of it. A path that names a type
    already reached is still recorded, because a TAB is asked about a path, not about a type.

    The cost is a few seconds for the whole tree, spent once per installation rather than once
    per TAB. Returns the number of nouns answered, which is what a caller compares between runs.
    """
    from office365.routing import navigations, nouns, route

    document = _document()
    answered = 0
    for product in products:
        published = nouns(product)
        document["nodes"][product] = _rows(_build(product, ()))
        reached: Dict[type, Tuple[str, ...]] = {}
        queue: List[Tuple[str, ...]] = [(entry.noun,) for entry in published.values()]
        while queue:
            path = queue.pop()
            found = route(product, *path)
            words = _words_of(found)
            document["nodes"][" ".join((product, *path))] = _rows(words)
            if words is None:
                continue
            here = found.here or found.entity
            if here in reached:
                continue
            reached[here] = path
            queue.extend(path + (word,) for word in navigations(here))
        answered += len(published)
        document["stamps"][product] = _stamp(product)
        _write(document)
        out(f"{product}: {len(published)} nouns, {len(reached)} types")
    return answered


def _build(product: str, path: "Sequence[str]") -> "Optional[Tuple[Candidate, ...]]":
    """Compute one node from the model: the nouns of a product, or one route's words."""
    from office365.routing import nouns, route

    if not path:
        published = nouns(product)
        return tuple(
            Candidate(entry.noun, "noun", entry.entity.__name__)
            for entry in sorted(published.values(), key=lambda entry: entry.noun)
        )
    return _words_of(route(product, *path))


def _words_of(found: "Any") -> "Optional[Tuple[Candidate, ...]]":
    """The words a route offers, or ``None`` where it ended on an action."""
    from office365.routing import navigations

    if found.verb is not None:
        return None
    links = navigations(found.here or found.entity)
    return tuple(
        Candidate(word, "action", found.commands[word][2].effect)
        if word in found.commands
        else Candidate(word, "navigation", links[word].__name__)
        for word in found.words
    )


def _rows(candidates: "Optional[Sequence[Candidate]]") -> "Optional[List[List[str]]]":
    """A node as JSON keeps it: one record per word, and nothing else."""
    if candidates is None:
        return None
    return [[candidate.word, candidate.kind, candidate.detail] for candidate in candidates]


def _thaw(node: "Optional[List[List[str]]]") -> "Optional[Tuple[Candidate, ...]]":
    """One node, read back from JSON."""
    if node is None:
        return None
    return tuple(Candidate(*item) for item in node)


@cache
def _document() -> "Dict[str, Any]":
    """The cache, read once per process; an unreadable or older one starts empty."""
    return _read()


def _read() -> "Dict[str, Any]":
    try:
        document = json.loads(cache_path().read_text("utf-8"))
    except (OSError, ValueError):
        return _empty()
    return document if document.get("format") == FORMAT else _empty()


def _empty() -> "Dict[str, Any]":
    return {"format": FORMAT, "stamps": {}, "nodes": {}}


def _remember(document: "Dict[str, Any]", product: str, key: str, candidates: "Optional[Sequence[Candidate]]") -> None:
    """Keep one node, stamped with the modules that were read to build it."""
    document["nodes"][key] = _rows(candidates)
    document["stamps"][product] = _stamp(product)
    _write(document)


def _stamp(product: str) -> "Dict[str, int]":
    """Module path -> mtime, for every module of ``product`` this process read.

    The dependency is the product's own modules and not just the ones a node needed: a noun
    exists only as a class somewhere under the package, so the set of nouns depends on files
    a single answer never imported, and a narrower stamp would go stale without noticing.
    """
    prefix = f"office365.{product}"
    stamp: "Dict[str, int]" = {}
    for name, module in list(sys.modules.items()):
        if not name.startswith(prefix):
            continue
        path = getattr(module, "__file__", None)
        try:
            stamp[path] = os.stat(path).st_mtime_ns  # type: ignore[arg-type]
        except (OSError, TypeError):
            continue
    return stamp


def _fresh(stamp: "Optional[Dict[str, int]]") -> bool:
    """Whether every module that produced the answers is still byte-for-byte where it was."""
    if not stamp:
        return False
    for path, mtime in stamp.items():
        try:
            if os.stat(path).st_mtime_ns != mtime:
                return False
        except OSError:
            return False
    return True


def cache_path() -> Path:
    """Where the cache lives: ``O365_CACHE``, then ``XDG_CACHE_HOME``, then ``~/.cache``."""
    override = os.environ.get("O365_CACHE")
    if override:
        return Path(override).expanduser()
    home = os.environ.get("XDG_CACHE_HOME") or "~/.cache"
    return Path(home).expanduser() / "o365" / "completion.json"


def _write(document: "Dict[str, Any]") -> None:
    """Save the cache; a directory that cannot be written costs latency, never an answer."""
    path = cache_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(document, separators=(",", ":")), "utf-8")
    except OSError:
        return


def script(shell: str, command: str = "o365") -> str:
    """The completion script for ``shell``, asking ``command`` for its words.

    Args:
        shell: one of :data:`SHELLS`.
        command: the program name the script completes, ``o365`` unless a caller renames it.

    Raises:
        LookupError: the shell is not one of :data:`SHELLS`.
    """
    try:
        template = {"bash": _BASH, "zsh": _ZSH, "fish": _FISH}[shell]
    except KeyError:
        raise LookupError(f"no completion script for {shell!r}; say one of: {', '.join(SHELLS)}") from None
    return template.replace("o365", command)


#: The one function command line name the three scripts share, so renaming the program is one
#: substitution and the protocol stays spelled in one place.
_BASH = """\
_o365() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local words=("${COMP_WORDS[@]:1:COMP_CWORD-1}")
    local candidates
    candidates=$(o365 __complete --prefix "$cur" ${words[@]+"${words[@]}"} 2>/dev/null)
    COMPREPLY=($(compgen -W "$candidates" -- "$cur"))
}
complete -F _o365 o365
"""

_ZSH = """\
#compdef o365

_o365() {
    local cur="${words[CURRENT]}"
    local -a candidates
    candidates=("${(@f)$(o365 __complete --prefix "$cur" "${(@)words[2,CURRENT-1]}" 2>/dev/null)}")
    (( ${#candidates} )) || return 1
    compadd -a candidates
}

if typeset -f compdef >/dev/null 2>&1; then
    compdef _o365 o365
else
    _o365 "$@"
fi
"""

_FISH = """\
function __o365_complete
    set -l words (commandline -opc)
    set -l prefix (commandline -ct)
    o365 __complete --describe --prefix $prefix $words[2..-1] 2>/dev/null
end
complete -c o365 -f -a '(__o365_complete)'
"""
