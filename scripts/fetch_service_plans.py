"""Refresh the service plan names the licence markers are checked against.

Microsoft publishes "Product names and service plan identifiers for licensing" as a CSV whose
``Service_Plan_Name`` column is the vocabulary ``subscribedSkus`` reports and
``@requires_license`` names. ``tests/data/service_plans.txt`` is that column, deduplicated and
sorted, so a marker can be checked against every plan the service publishes without a network
call in the test suite.

    python scripts/fetch_service_plans.py            # write tests/data/service_plans.txt
    python scripts/fetch_service_plans.py --from /tmp/plans.csv

Re-run it when a marker names a plan that is not in the file: either the name is spelled as the
service does not spell it (the point of the check), or Microsoft published a new plan and the
file is one day older than the API.
"""

from __future__ import annotations

import argparse
import csv
import io
import pathlib
import urllib.request

URL = (
    "https://download.microsoft.com/download/e/3/e/e3e9faf2-f28b-490a-9ada-c6089a1fc5b0/"
    "Product%20names%20and%20service%20plan%20identifiers%20for%20licensing.csv"
)
DESCRIPTION = "Refresh the service plan names the licence markers are checked against"
TARGET = pathlib.Path(__file__).resolve().parents[1] / "tests" / "data" / "service_plans.txt"
COLUMN = "Service_Plan_Name"
HEADER = """# Service plan names Microsoft publishes for licensing, one per line.
# Source: Product names and service plan identifiers (learn.microsoft.com/licensing-service-plan)
# Refresh: python scripts/fetch_service_plans.py
"""


def fetch(source: str | None) -> bytes:
    """The CSV bytes: read from ``source`` when given, downloaded otherwise."""
    if source is not None:
        return pathlib.Path(source).read_bytes()
    with urllib.request.urlopen(URL, timeout=60) as response:  # noqa: S310 - the published CSV
        return response.read()


def names(raw: bytes) -> list[str]:
    """The distinct service plan names in ``raw``, sorted."""
    rows = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    return sorted({row[COLUMN].strip() for row in rows if row[COLUMN].strip()})


def main() -> None:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--from", dest="source", help="read a CSV already on disk")
    options = parser.parse_args()
    written = names(fetch(options.source))
    TARGET.write_text(HEADER + "".join(f"{name}\n" for name in written), encoding="utf-8")
    print(f"{TARGET.relative_to(TARGET.parents[2])}: {len(written)} service plan names")


if __name__ == "__main__":
    main()
