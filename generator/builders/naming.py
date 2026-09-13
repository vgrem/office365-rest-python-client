from __future__ import annotations

import builtins
import keyword
import re


def to_snake_case(name: str, avoid_keywords: bool = True) -> str:
    """Converts a PascalCase/camelCase identifier to snake_case.

    Handles acronyms and plural acronyms:

    * ``emailIDs`` -> ``email_ids``, ``APIs`` -> ``apis``, ``URLs`` -> ``urls``
    * ``HTTPServer`` -> ``http_server``, ``UTCToLocalTime`` -> ``utc_to_local_time``

    Args:
        name: Identifier to convert.
        avoid_keywords: When true, append ``_`` to Python keywords/builtins so the
            result is a valid attribute/parameter name.
    """
    # lower -> upper boundary (emailIDs -> email_IDs)
    s1 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    # single capital followed by a word (ASite -> A_Site, IFollowed -> I_Followed)
    s2 = re.sub(r"([A-Z])([A-Z][a-z]{2,})", r"\1_\2", s1)
    # acronym followed by a short word (UTCTo -> UTC_To); 's' is excluded so that
    # plural acronyms (IDs, URLs, APIs) are not split
    s3 = re.sub(r"([A-Z]{2,})([A-Z][a-rt-z])", r"\1_\2", s2)
    # merge a leading single lowercase word (iCalUId -> ical_uid) before lowercasing
    snake_case = re.sub(r"^([a-z])_", r"\1", s3).lower()
    if avoid_keywords and (keyword.iskeyword(snake_case) or hasattr(builtins, snake_case)):
        return snake_case + "_"
    return snake_case
