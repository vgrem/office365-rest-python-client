"""Credential doctor.

Reports which authentication flows are configured and exits non-zero when a
required one is missing::

    python -m tests.doctor
    python -m tests.doctor --require app-only-cert
"""

from __future__ import annotations

import argparse
import sys

from tests.settings import FLOWS, settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report which authentication flows are configured.")
    parser.add_argument(
        "--require",
        choices=list(FLOWS),
        action="append",
        metavar="FLOW",
        help="exit non-zero unless FLOW is configured (repeatable)",
    )
    args = parser.parse_args(argv)

    print(settings.format_readiness())

    missing = [flow for flow in (args.require or []) if not settings.is_ready(flow)]
    if missing:
        print(f"\nERROR: required flow(s) not configured: {', '.join(missing)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
