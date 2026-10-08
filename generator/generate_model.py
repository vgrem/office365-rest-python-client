"""Generate the client model from OData metadata.

Run as ``python -m generator.generate_model <service> [--dry-run]``. The
implementation lives in :mod:`generator.cli` / :mod:`generator.pipeline`.
"""

from __future__ import annotations

from generator.cli import generate, main

__all__ = ["generate", "main"]

if __name__ == "__main__":
    raise SystemExit(main())
