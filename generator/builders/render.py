"""Post-processing of generated source.

``ast.unparse`` emits ``'single'`` string literals, while the codebase (and
``ruff format``) uses ``"double"`` and only falls back to single quotes when the
value itself contains a double quote. Re-quoting here keeps regenerated files
stable against the committed style instead of churning every string literal.
"""

from __future__ import annotations

import ast
import io
import json
import tokenize

_TRIPLE_QUOTES = ('"""', "'''")


def normalize_quotes(source: str) -> str:
    """Rewrite simple string literals to the project's quote style.

    Docstrings, bytes literals, raw strings and f-strings are left untouched.
    """
    tokens = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        emitted = token
        if token.type == tokenize.STRING:
            requoted = _requote(token.string)
            if requoted != token.string:
                emitted = tokenize.TokenInfo(token.type, requoted, token.start, token.end, token.line)
        tokens.append(emitted)
    return tokenize.untokenize(tokens)


def _requote(literal: str) -> str:
    prefix, body = _split_prefix(literal)
    if body.startswith(_TRIPLE_QUOTES) or prefix.lower() == "r":
        return literal
    try:
        value = ast.literal_eval(literal)
    except (SyntaxError, ValueError):
        return literal
    if not isinstance(value, str):
        return literal
    return prefix + _quote(value)


def _quote(value: str) -> str:
    """Double-quoted literal, but single quotes when the value contains ``"``."""
    if '"' in value and "'" not in value:
        return repr(value)
    return json.dumps(value, ensure_ascii=False)


def _split_prefix(literal: str) -> tuple[str, str]:
    index = 0
    while index < len(literal) and literal[index].isalpha():
        index += 1
    return literal[:index], literal[index:]
