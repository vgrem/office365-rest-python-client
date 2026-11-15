"""The model's discovery answers, written once so a command line can read them in milliseconds.

A command line asks the model a handful of questions before it sends anything: which products
exist, which nouns one publishes, what a noun answers and holds, and whether a client can walk
to it at all. Today each answer costs an import of the product packages - 22 packages, 6 557
modules, 7.3 s measured here - and none of them depends on the request. So they are written
once and read as data: ``office365/index.json``, which parses in 4 ms.

Four rules, because a derived index is a claim that it still agrees with the model:

* **Generated, never hand-edited.** ``generator graph --index`` is its only writer, and every
  value is :mod:`office365.routing`'s own answer - the function a command calls when it does
  import - so the file and the router cannot drift into two vocabularies.
* **A re-render is byte-identical.** Products, nouns and every list inside a record are sorted,
  so a filesystem that walks its files in another order writes the same file;
  ``tests/tooling/test_generator_index.py`` compares the shipped file with a fresh build
  instead of trusting the commit.
* **Discovery only.** The index says what exists and where a walk lands. A command that sends
  still reads the type: a flag is a parameter, a column is what ``TypeSchema`` says ``$select``
  takes, and the URL comes from the annotations.
* **Version-stamped.** :data:`FORMAT` and the library version travel in the file, so a reader
  upgraded past the model that rendered it can tell.

One noun per line, which is why the writer is not :func:`generator.core.report.write_json`: an
indented list spends three lines on one noun's columns, so a change of one noun would read as a
hundred-line rewrite of a 1 MB file.
"""

from __future__ import annotations

import importlib
import json
import pkgutil
import re
from importlib import metadata
from pathlib import Path
from typing import Any, Dict, Mapping

#: The index layout, bumped when an older file would be read as this one.
FORMAT = 1

#: The artefact, relative to the repository root.
DEFAULT_PATH = "office365/index.json"

#: The package tree the index describes.
ROOT = "office365"

#: The distribution whose version is stamped, when the tree is installed.
DISTRIBUTION = "office365-rest-python-client"


def build_index() -> Dict[str, Any]:
    """The document for the tree as it is now: every product, its nouns, and what each noun is."""
    from office365.routing import nouns, products

    clients = _clients()
    reached = _walks(clients)
    return {
        "format": FORMAT,
        "library": _library_version(),
        "root": ROOT,
        "roots": {name: client.__module__ for name, client in clients.items()},
        "products": {
            product: {key: _noun(found, reached) for key, found in sorted(nouns(product).items())}
            for product in products()
        },
    }


def write_index(path: str | Path, document: Mapping[str, Any]) -> Path:
    """Write the document one noun per line, and answer the path it was written to."""
    head = {key: value for key, value in document.items() if key != "products"}
    blocks = []
    for product, entries in document["products"].items():
        records = [f"{json.dumps(key)}:{json.dumps(record, separators=(',', ':'))}" for key, record in entries.items()]
        blocks.append(f"{json.dumps(product)}:{{\n" + ",\n".join(records) + "\n}")
    # the head's own closing brace is dropped so ``products`` can be appended as a sibling
    text = f'{json.dumps(head, separators=(",", ":"))[:-1]},"products":{{\n' + ",\n".join(blocks) + "\n}}\n"
    target = Path(path)
    target.write_text(text, encoding="utf-8")
    return target


def render_index(document: Mapping[str, Any], path: Path) -> str:
    """One line: what was written, and how much of it a command can walk to."""
    products = document["products"]
    nouns = sum(len(entries) for entries in products.values())
    walkable = sum(1 for entries in products.values() for record in entries.values() if record.get("walks"))
    return (
        f"{nouns} nouns over {len(products)} products, {walkable} walkable -> {path}"
        f" ({path.stat().st_size / 1e6:.1f} MB)"
    )


def _noun(found: Any, reached: Mapping[str, Mapping[type, tuple[str, ...]]]) -> Dict[str, Any]:
    """One noun: what it is, what it answers, what it holds, and how a client walks to it."""
    from office365.routing import navigations
    from office365.runtime.schema import TypeSchema

    record: Dict[str, Any] = {
        "noun": found.noun,
        "type": _ref(found.entity),
        "verbs": sorted(found.commands),
        "columns": sorted(TypeSchema.of(found.entity).columns),
        "navigations": {word: _ref(held) for word, held in sorted(navigations(found.entity).items())},
    }
    if found.collection is not None:
        record["collection"] = _ref(found.collection)
    walks = _walks_of(found, reached)
    if walks:
        record["walks"] = walks
    return record


def _walks_of(found: Any, reached: Mapping[str, Mapping[type, tuple[str, ...]]]) -> Dict[str, Dict[str, Any]]:
    """The clients that reach this noun, and the words to walk, item and feed kept apart.

    Both halves are recorded because they answer different commands: a listing wants the feed
    (``me.messages`` is a ``MessageCollection``), reading one object wants the item. A noun no
    client reaches is left without a ``walks`` key - the honest answer to "may a command run
    this" is no, and it is the answer for 1 687 of the 2 036 nouns.
    """
    walks: Dict[str, Dict[str, Any]] = {}
    for name, paths in reached.items():
        halves: Dict[str, Any] = {}
        if found.entity in paths:
            halves["item"] = list(paths[found.entity])
        if found.collection is not None and found.collection in paths:
            halves["feed"] = list(paths[found.collection])
        if halves:
            walks[name] = halves
    return walks


def _clients() -> Dict[str, type]:
    """The classes a walk may start at: every ``ClientRuntimeContext`` the tree defines.

    Read from the modules that define them, not from a list here. A client is a root because
    the model says a request starts there; which audience spends a token on it is a command
    line's own choice (``office365.cli.AUDIENCES``), not a model fact. The library's own base
    class is not a client: nobody holds one.
    """
    from office365.runtime.client_runtime_context import ClientRuntimeContext

    package = importlib.import_module(ROOT)
    found: Dict[str, type] = {}
    for info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        try:
            module = importlib.import_module(info.name)
        except Exception:  # a module the tree cannot import at all defines no client
            continue
        for member in vars(module).values():
            if isinstance(member, type) and member.__module__ == info.name:
                if issubclass(member, ClientRuntimeContext) and member is not ClientRuntimeContext:
                    found.setdefault(member.__name__, member)
    return dict(sorted(found.items()))


def _walks(clients: Mapping[str, type]) -> Dict[str, Dict[type, tuple[str, ...]]]:
    """For each client, the shortest walk to every type it reaches.

    One breadth-first pass per client, not one per noun, over the same edges
    :func:`office365.routing.chain` walks: a link is a property that says what it holds, so
    the graph is read once here and shipped.
    """
    from office365.routing import navigations

    reached: Dict[str, Dict[type, tuple[str, ...]]] = {}
    for name, client in clients.items():
        paths: Dict[type, tuple[str, ...]] = {client: ()}
        queue = [client]
        while queue:
            current = queue.pop(0)
            for word, held in navigations(current).items():
                if held not in paths:
                    paths[held] = paths[current] + (word,)
                    queue.append(held)
        reached[name] = paths
    return reached


def _ref(cls: type) -> str:
    """A type as ``module:name``, which is how a reader imports it back."""
    return f"{cls.__module__}:{cls.__name__}"


def _library_version() -> str:
    """The version of the model the index was rendered from.

    Read from the installed distribution, because that is what a reader compares its own
    version to; a checkout that was never installed falls back to ``pyproject.toml``.
    """
    try:
        return metadata.version(DISTRIBUTION)
    except metadata.PackageNotFoundError:
        manifest = Path(__file__).resolve().parents[2] / "pyproject.toml"
        stated = re.search(r'^version = "([^"]+)"', manifest.read_text("utf-8"), re.MULTILINE)
        return stated.group(1) if stated else "unknown"
