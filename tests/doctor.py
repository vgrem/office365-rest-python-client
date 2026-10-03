"""Credential doctor.

Reports which authentication flows are configured and exits non-zero when a
required one is missing::

    python -m tests.doctor
    python -m tests.doctor --require app-only-cert
"""

from __future__ import annotations

import argparse
import sys

from tests.settings import FLOWS, Settings, settings


def _format_status(config: Settings) -> str:
    """Render a human-readable readiness report for all flows."""
    ready = config.readiness()
    width = max(len(flow.label) for flow in FLOWS.values())
    lines = ["Auth readiness (environment + .env):"]
    for flow, spec in FLOWS.items():
        missing = ready[flow]
        status = "ready" if not missing else "not ready"
        detail = "" if not missing else "  missing: " + ", ".join(missing)
        lines.append(f"  {spec.label:<{width}}  {status:<9}{detail}")
    if all(ready.values()):  # every flow is missing at least one requirement
        lines.append("")
        lines.append("  Tip: cp .env.example .env, fill it in, then re-run `python -m tests.doctor`.")
    return "\n".join(lines)


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

    print(_format_status(settings))

    missing = [flow for flow in (args.require or []) if not settings.is_ready(flow)]
    if missing:
        print(f"\nERROR: required flow(s) not configured: {', '.join(missing)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
