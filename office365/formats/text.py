"""The text of a content line: escaping, folding, and the parameter value.

Three rules, each of which the two writers had their own version of — and in two of the
three the versions disagreed, which is why this module exists rather than a shared helper
imported from one of them:

* :func:`escape_text` — RFC 5545 §3.3.11 and RFC 6350 §3.4 escape the same four things
  (``\\``, ``;``, ``,`` and a line break) in a TEXT value. A lone ``\\r`` is a line break
  too: the vCard copy only matched ``\\r?\\n``, so a value carrying a bare carriage return
  had it written raw into the document.
* :func:`fold_line` — both impose RFC 5545 §3.1's (and RFC 6350 §3.1's) 75 octets, and
  disagreed about the first line: one reserved the continuation's leading space on every
  line, so the first was 74 octets; the other spent all 75. The allowance is the rule, so
  the first line takes 75 and every continuation takes 74 of content behind its space.
* :func:`quote_param` — a parameter is not a TEXT value and takes no backslashes, so it
  needs an encoding of its own; see its docstring. One writer had none, which is how a
  display name could end the line it was written on.

Folding and measuring are done on UTF-8 octets and applied at character boundaries: a
line is capped in octets, and a multi-byte character is never split across the fold.
"""

from __future__ import annotations

from typing import Any

#: RFC 5545 §3.1 and RFC 6350 §3.1 cap a content line at 75 octets, line break excluded.
MAX_LINE_OCTETS = 75

#: RFC 6868's caret escapes: the three characters a parameter value cannot hold. The
#: caret itself goes first, so an escape is never re-escaped by a later pass.
_CARET_ESCAPES = (("^", "^^"), ("\r\n", "^n"), ("\r", "^n"), ("\n", "^n"), ('"', "^'"))


def escape_text(value: Any) -> str:
    """Escape a TEXT value (RFC 5545 §3.3.11, RFC 6350 §3.4): ``\\``, ``;``, ``,``, newline."""
    text = "" if value is None else str(value)
    text = text.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
    return text.replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n")


def fold_line(line: str) -> str:
    """Fold a content line so no line exceeds 75 octets, continuing behind a space.

    The first line carries up to 75 octets; each continuation spends one of its own 75 on
    the leading space, so it carries 74 of the value. A character is never split — the
    budget is counted in encoded octets and spent at character boundaries.
    """
    if len(line.encode("utf-8")) <= MAX_LINE_OCTETS:
        return line
    chunks: list[str] = []
    current: list[str] = []
    size = 0
    for char in line:
        width = len(char.encode("utf-8"))
        if size + width > MAX_LINE_OCTETS:
            chunks.append("".join(current))
            current, size = [" ", char], 1 + width
        else:
            current.append(char)
            size += width
    chunks.append("".join(current))
    return "\r\n".join(chunks)


def quote_param(value: Any) -> str:
    """A parameter value: caret-encoded, quoted, and free of control characters.

    ``CN=`` used to be built by interpolation, which is a content-line injection: a
    display name of ``Bob "Bobby"`` closed the quoted-string early, and a name carrying a
    line break started a line of its own — a property the reader would honour. Calling
    :func:`escape_text` does not help: a parameter is not a TEXT field and takes no
    backslashes, and a quoted-string may not contain a DQUOTE at all. RFC 6868's carets
    carry the three casualties — ``^'`` is a DQUOTE, ``^^`` a caret, ``^n`` a line break —
    so a reader without the escapes shows ``^'`` where a reader without quoting showed a
    truncated name and a forged property.

    Any other control character is dropped — a tab is legal inside a quoted-string but is
    not a name — and the sidecar keeps the name exactly as the service sent it.
    """
    text = "" if value is None else str(value)
    for raw, escaped in _CARET_ESCAPES:
        text = text.replace(raw, escaped)
    text = "".join(char for char in text if char >= " " and char != "\x7f")
    return f'"{text}"'


__all__ = ["MAX_LINE_OCTETS", "escape_text", "fold_line", "quote_param"]
