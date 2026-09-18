"""Path | file-like resolution shared by the format readers/writers.

Pandas-style: every reader/writer accepts a filesystem path, a ``PathLike`` or an
already-open file object. Binary vs text mode is chosen by the format; an
existing stream is passed through untouched.
"""

from __future__ import annotations

from contextlib import contextmanager
from os import PathLike
from typing import IO, Any, Iterator, Union, cast

Source = Union[str, PathLike, IO[Any]]


def is_stream(source: Any) -> bool:
    """Whether ``source`` is an already-open file object (vs a path)."""
    return hasattr(source, "read") or hasattr(source, "write")


@contextmanager
def open_text(source: Source, mode: str = "r", **kwargs: Any) -> Iterator[IO[Any]]:
    """Yield a text stream for ``source`` (a path is opened, a stream passed through)."""
    if is_stream(source):
        yield source  # type: ignore[misc]
        return
    kwargs.setdefault("encoding", "utf-8")
    if "b" not in mode:
        kwargs.setdefault("newline", "")
    with open(cast(Any, source), mode, **kwargs) as f:
        yield f


@contextmanager
def open_binary(source: Source, mode: str = "rb", **kwargs: Any) -> Iterator[IO[Any]]:
    """Yield a binary stream for ``source`` (a path is opened, a stream passed through)."""
    if is_stream(source):
        yield source  # type: ignore[misc]
        return
    with open(cast(Any, source), mode, **kwargs) as f:
        yield f
