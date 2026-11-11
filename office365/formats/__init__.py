"""Rendered documents: the line mechanics every ``.ics`` and ``.vcf`` shares.

A calendar entry and a contact card are the same kind of artefact — a line-oriented text
document with a 75-octet fold, backslash-escaped TEXT values and caret-encoded
parameters — and each writer grew its own copy of that mechanics. This package is the one
copy: a fix to a fold, an escape or a parameter is a fix to both documents at once, and
the RFC numbers are stated where they are implemented rather than per writer.
"""

from office365.formats.text import MAX_LINE_OCTETS, escape_text, fold_line, quote_param

__all__ = ["MAX_LINE_OCTETS", "escape_text", "fold_line", "quote_param"]

#: Text and data formats the library reads and writes, not a service.
__product__ = ""
