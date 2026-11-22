"""How much of the model a command line can reach, measured by verb role.

Reads the library rather than the index, because the question is about *routes*: every method a
product stamps with a verb, and whether a line of words can build a URL for it. Three answers,

* ``walk`` - the links name the object (``me.messages``, ``device_management.managed_devices``);
* ``--id`` - the feed is named but its item is an argument (``users[<id>]``, ``messages[<id>]``);
* ``none``  - the type is constructed nowhere in the model, so no line can address it.

    python scripts/walks.py

The numbers are what ``docs/cli.md`` quotes for what a command can and cannot name.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import replace
from typing import Any

from office365 import cli, routing


def census() -> "Counter[tuple[str, str]]":
    """``(role, fate)`` -> how many stamped methods answer that way."""
    counted: Counter[tuple[str, str]] = Counter()
    for product in routing.products():
        try:
            index = routing.nouns(product)
        except LookupError:  # a package that publishes no nouns is not a product
            continue
        for noun in index.values():
            root = cli._root(cli._audience(noun.entity))
            for _, (half, method, verb) in noun.commands.items():
                found = replace(noun, verb=verb, here=half, method=method)
                counted[(verb.role, fate(root, found, product))] += 1
    return counted


def fate(root: type, found: Any, product: str) -> str:
    if cli._walk(root, found) is not None:
        return "walk"
    if cli._keyed(found, getattr(found.here, found.method)) and cli._feed(root, found, product) is not None:
        return "id"
    return "none"


def main() -> None:
    counted = census()
    roles = sorted({role for role, _ in counted})
    print(f"{'role':<10}{'walk':>7}{'--id':>7}{'none':>7}")
    for role in roles:
        print(f"{role:<10}{counted[(role, 'walk')]:>7}{counted[(role, 'id')]:>7}{counted[(role, 'none')]:>7}")
    print(
        f"{'total':<10}{sum(v for (r, f), v in counted.items() if f == 'walk'):>7}"
        f"{sum(v for (r, f), v in counted.items() if f == 'id'):>7}"
        f"{sum(v for (r, f), v in counted.items() if f == 'none'):>7}"
    )


if __name__ == "__main__":
    main()
