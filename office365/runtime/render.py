"""What a command line prints, and why it looks like that.

``display.py`` renders an object *inside* a notebook: bounded, indented, prefixed with the
class name -- a preview of a Python value. A terminal asks for something else, and the
difference is not cosmetic: a header row a reader can scan, numbers that line up, elision
marked so a truncated name is not mistaken for a short one, a sentence when there is
nothing to show, and a column that opens in a browser.

So the two renderers are separate rather than one with flags. Everything here takes
**already-loaded payloads** -- no function imports the model, so printing cannot trigger a
request, and what a table shows is exactly what the response carried.

The formats are the ones a mature command line offers (``kubectl -o wide|json|name``,
``gh --json``, ``docker --format``): ``table`` is the default, ``wide`` is every loaded
field, ``json``/``csv``/``tsv`` are for other programs, and ``url``/``name`` are for
``xargs``.
"""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Iterable, Mapping, Sequence
from datetime import date, datetime
from enum import Enum
from typing import Any
from urllib.parse import urlsplit

#: The formats ``-o`` accepts. ``table`` is the default; ``wide`` is the same table with
#: every field the payload carried and no truncation.
FORMATS = ("table", "wide", "json", "csv", "tsv", "url", "name")

#: The fallback vocabulary of address columns, for a caller that has no type to ask.
#: A caller that *has* one passes ``TypeSchema.links`` -- the ``link`` facet -- and that
#: declaration decides; this tuple is only what to do when no type was named. What it must
#: never become again is the authority: the CLI used to keep this list, and a type could not
#: say that its own column was an address. A server-relative value (``/sites/x/Lists/y``) has
#: the site's origin joined to it, so the printed link is one a person can open.
LINK_FIELDS = ("WebUrl", "Url", "DefaultViewUrl", "Path")

#: How many fields a table shows when nobody said which (`-o wide` lifts it).
MAX_COLUMNS = 8

#: Where a cell is cut, marked with ``…``. `kubectl` never truncates and `gh` does; a
#: listing of 146 lists with 60-character titles is unreadable unbounded, so the default
#: cuts and says so.
COLUMN_WIDTH = 48

#: How many fields a single object prints before it summarises the rest.
VERTICAL_FIELDS = 24

#: Two spaces: one column separator, wide enough for a header to read as one block.
_GAP = "  "

#: The OSC-8 hyperlink: the terminal draws ``text``, the link behind it is ``url``. Emitted
#: only when asked for -- a pipe must never receive escape codes.
_LINK_ON = "\033]8;;{}\033\\"
_LINK_OFF = "\033]8;;\033\\"


def origin_of(service_root_url: str | None) -> str:
    """The ``scheme://host`` a server-relative link is joined to, or ``""``."""
    if not service_root_url:
        return ""
    parts = urlsplit(service_root_url)
    return f"{parts.scheme}://{parts.netloc}" if parts.scheme and parts.netloc else ""


def resolve(
    payload: Mapping[str, Any],
    origin: str = "",
    resource_url: str | None = None,
    fields: Sequence[str] = LINK_FIELDS,
) -> str | None:
    """The URL a record stands for: a declared one if it carries it, else where it lives.

    ``resource_url`` is the object's own REST address (``.../_api/Web/Lists(guid'..')``).
    It is the last resort and only when it is a page a browser can show: a Graph URL or an
    ``_api`` path would open as JSON, so those answer ``None`` and the row gets no link.
    """
    absolute = relative = None
    for name in fields:
        value = payload.get(name)
        if not isinstance(value, str):
            continue
        value = value.strip()
        if not value:
            continue
        if value.startswith(("http://", "https://")):
            absolute = absolute or value
            continue
        if value.startswith("/") and origin:
            relative = relative or origin + value
    if absolute or relative:
        return absolute or relative
    if resource_url and "/_api/" not in resource_url and "graph.microsoft.com" not in resource_url:
        return resource_url
    return None


def hyperlink(url: str, text: str) -> str:
    """``text``, carrying ``url``: drawn as a link by every terminal that reads OSC-8."""
    return _LINK_ON.format(url) + text + _LINK_OFF


def _inline(value: Any) -> str:
    """A container as one cell: JSON, so a nested value is legible rather than a repr."""
    return json.dumps(value, default=str, ensure_ascii=False)


def cell(value: Any) -> tuple[str, bool]:
    """``(text, is_number)`` for one value: numbers align right, everything else left.

    The spellings are the ones a reader of a command line expects rather than Python's:
    ``true``/``false`` because that is what ``-o json`` prints next to it, ``yes``/``no``
    for nothing, an ISO timestamp without its microseconds.
    """
    if value is None:
        return "", False
    if isinstance(value, bool):
        return ("true" if value else "false"), False
    if isinstance(value, Enum):
        return str(value.name), False
    if isinstance(value, datetime):
        return value.isoformat(sep=" ", timespec="seconds"), False
    if isinstance(value, date):
        return value.isoformat(), False
    if isinstance(value, (int, float)):
        return str(value), True
    if isinstance(value, (Mapping, list, tuple)):
        return _inline(value), False
    return str(value).replace("\n", " "), False


def _union(records: Sequence[Mapping[str, Any]], limit: int | None) -> list[str]:
    """The fields the records actually carry, in first-seen order, bounded by ``limit``."""
    columns: list[str] = []
    for record in records:
        for name in record:
            if name not in columns:
                columns.append(name)
    return columns if limit is None else columns[:limit]


def _widths(columns: Sequence[str], rows: Sequence[Sequence[tuple[str, bool]]], width: int | None) -> list[int]:
    """The width each column needs: its widest cell, or its header, capped at ``width``."""
    widths = []
    for index, column in enumerate(columns):
        needed = max([len(column), *(len(row[index][0]) for row in rows)])
        widths.append(needed if width is None else min(needed, width))
    return widths


def _line(cells: Sequence[tuple[str, bool]], widths: Sequence[int], *, header: bool = False) -> str:
    """One rendered row: numeric cells pushed right, over-long cells elided with ``…``."""
    parts = []
    for index, (text, number) in enumerate(cells):
        width = widths[index]
        shown = text[: width - 1] + "…" if len(text) > width else text
        parts.append(shown.rjust(width) if number and not header else shown.ljust(width))
    return _GAP.join(parts).rstrip()


def table(
    records: Sequence[Mapping[str, Any]],
    columns: Sequence[str] | None = None,
    *,
    links: Sequence[str | None] | None = None,
    headers: bool = True,
    width: int | None = COLUMN_WIDTH,
    limit: int | None = MAX_COLUMNS,
) -> str:
    """Render records as an aligned table.

    Args:
        columns: The names to show, in that order. ``None`` shows the first-seen union,
            bounded by ``limit`` -- which is what a type that ranks no columns gets.
        links: One URL per record, or ``None``; when given, the first column's text carries
            it, because the first column is the name a reader clicks.
        headers: Whether the header row is printed (``--no-headers``).
        width: The widest a cell may be, or ``None`` to print values whole.
        limit: How many columns the union may reach, or ``None`` for all of them.
    """
    chosen = list(columns) if columns is not None else _union(records, limit)
    if not chosen:
        return ""
    rows = [[cell(record.get(name)) for name in chosen] for record in records]
    widths = _widths(chosen, rows, width)
    lines = [_line([(name.upper(), False) for name in chosen], widths, header=True)] if headers else []
    for index, row in enumerate(rows):
        line = _line(row, widths)
        url = links[index] if links and index < len(links) else None
        if url:
            text, _ = row[0]
            shown = text[: widths[0] - 1] + "…" if len(text) > widths[0] else text
            # The link wraps the name and never its padding: a terminal that marks a hyperlink
            # (a dotted underline in most) would otherwise draw a rule across the whole column,
            # which reads as a border between the rows rather than as a clickable title.
            pad = " " * (widths[0] - len(shown))
            line = (hyperlink(url, shown) + pad + line[widths[0] :]).rstrip()
        lines.append(line)
    return "\n".join(lines)


def vertical(
    payload: Mapping[str, Any],
    columns: Sequence[str] | None = None,
    *,
    link: str | None = None,
    limit: int | None = VERTICAL_FIELDS,
) -> str:
    """One object as aligned ``name  value`` lines -- a table of one row hides every field it has."""
    names = (["URL"] if link else []) + (list(columns) if columns is not None else list(payload))
    shown = names if limit is None else names[:limit]
    if not shown:
        return ""
    width = max(len(name) for name in shown)
    lines = []
    for name in shown:
        text, _ = cell(link if name == "URL" and link else payload.get(name))
        # The address line and any field that spells the same address carry the link; nothing
        # else does, so a value that merely looks like a URL is printed as text.
        carried = link if link and (name == "URL" or text == link) else None
        lines.append(f"{name.ljust(width)}{_GAP}{hyperlink(carried, text) if carried else text}".rstrip())
    if len(shown) < len(names):
        lines.append(f"{'…'.ljust(width)}{_GAP}(+{len(names) - len(shown)} more fields, -o json)")
    return "\n".join(lines)


def delimited(records: Sequence[Mapping[str, Any]], columns: Sequence[str] | None, delimiter: str) -> str:
    """CSV/TSV: the same columns, quoted as the format requires, so a pipe can read them."""
    chosen = list(columns) if columns is not None else _union(records, None)
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=delimiter, lineterminator="\n")
    writer.writerow(chosen)
    for record in records:
        writer.writerow([cell(record.get(name))[0] for name in chosen])
    return buffer.getvalue().rstrip("\n")


def render(
    payloads: Sequence[Mapping[str, Any]],
    fmt: str = "table",
    *,
    columns: Sequence[str] | None = None,
    links: Sequence[str | None] | None = None,
    origin: str = "",
    resources: Sequence[str | None] | None = None,
    fields: Sequence[str] = LINK_FIELDS,
    link: str = "auto",
    headers: bool = True,
    tty: bool = False,
    empty: str = "",
    width: int | None = COLUMN_WIDTH,
) -> str:
    """Render ``payloads`` in ``fmt``: the one entry a command calls.

    Args:
        columns: Names to show, or ``None`` to let the type (via the caller) or the payload
            decide. ``-o wide`` means the caller passes ``None`` and ``limit=None``.
        links: URLs per record, already resolved; computed here when ``None``.
        origin: ``scheme://host`` for server-relative links.
        resources: The objects' REST addresses, the last resort for a link.
        fields: The columns that hold an address, from ``TypeSchema.links`` of the type
            being printed; the default is the vocabulary used when no type was named.
        link: ``auto`` (a terminal), ``always``, or ``never``.
        tty: Whether stdout is a terminal; only ``link=auto`` reads it.
        empty: What to print when there is nothing -- a sentence, never nothing.
        width: Where a cell is cut. ``None`` prints identifiers - a permission name is not a
            title to shorten - and ``-o wide`` means the same.
    """
    if not payloads:
        # A machine format answers with its own empty document, because the sentence is for a
        # reader: `o365 … -o json | jq` has to receive `[]`, not English. csv and tsv answer with
        # nothing, which is what a spreadsheet calls zero rows.
        return "[]" if fmt == "json" else "" if fmt in ("csv", "tsv", "url", "name") else empty
    if fmt == "json":
        return json.dumps(list(payloads), indent=2, default=str, ensure_ascii=False)
    if fmt in ("csv", "tsv"):
        return delimited(payloads, columns, "," if fmt == "csv" else "\t")
    urls = (
        list(links)
        if links is not None
        else [
            resolve(payload, origin, resources[index] if resources and index < len(resources) else None, fields)
            for index, payload in enumerate(payloads)
        ]
    )
    if fmt == "url":
        return "\n".join(url or "" for url in urls)
    if fmt == "name":
        chosen = list(columns) if columns is not None else _union(payloads, 1)
        return "\n".join(cell(payload.get(chosen[0]))[0] for payload in payloads) if chosen else ""
    if fmt == "table" and len(payloads) == 1 and columns is None:
        live = urls[0] if link == "always" or (link == "auto" and tty) else None
        return vertical(payloads[0], None, link=live)
    shown = urls if link == "always" or (link == "auto" and tty) else None
    return table(
        payloads,
        columns,
        links=shown,
        headers=headers,
        width=None if fmt == "wide" else width,
        limit=None if fmt == "wide" else MAX_COLUMNS,
    )


def one_per_line(values: Iterable[Any]) -> str:
    """``url``/``name`` output for values the caller already extracted."""
    return "\n".join(str(value) for value in values)
