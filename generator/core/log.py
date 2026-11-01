"""Logging for the generator: status text goes through one named logger.

Report output the user asked for (rendered plans, suggestions) stays on stdout via
``print``; progress and diagnostic messages use :data:`log`, so a caller (or a test)
decides what to show. The CLI installs a message-only stdout handler, which keeps the
console output identical to what the tool printed before.
"""

from __future__ import annotations

import logging
import sys

log = logging.getLogger("generator")


def configure(verbose: bool = False) -> None:
    """Send generator messages to stdout as plain text (idempotent)."""
    log.setLevel(logging.DEBUG if verbose else logging.INFO)
    if any(getattr(handler, "_generator_cli", False) for handler in log.handlers):
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    handler._generator_cli = True  # type: ignore[attr-defined]
    log.addHandler(handler)
    log.propagate = False
