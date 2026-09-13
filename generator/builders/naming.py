from __future__ import annotations

import builtins
import keyword
import re


def to_snake_case(name: str, avoid_keywords: bool = True) -> str:
    """Converts a PascalCase/camelCase identifier to snake_case.

    Args:
        name: Identifier to convert.
        avoid_keywords: When true, append ``_`` to Python keywords/builtins so the
            result is a valid attribute/parameter name.
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    snake_case = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    if avoid_keywords and (keyword.iskeyword(snake_case) or hasattr(builtins, snake_case)):
        return snake_case + "_"
    return snake_case
