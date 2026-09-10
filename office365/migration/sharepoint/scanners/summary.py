"""Site collection scan summary — the SharePoint ``SITE``-container payload.

Built by the SharePoint walkers (single-site and tenant) and handed to
``SITE``-container scans once the whole subtree has settled.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SiteScanSummary:
    """The site collection's scan state, aggregated by the walker.

    Built as the walker visits the site collection (usage), its web tree
    (``web_count``) and every list (``item_count``, ``last_modified``); handed
    to ``SITE``-container scans once the whole subtree has settled.

    The tenant walker populates it from ``SiteProperties`` instead and sets
    ``report_impacted_only`` so SMAT-style scans only list impacted sites
    (e.g. LargeSites lists only collections over the threshold, and locked
    ones are surfaced by the LockedSites scan).
    """

    site_id: str | None = None
    site_url: str | None = None
    owner: str | None = None
    admins: str | None = None
    storage_bytes: int | None = None
    hits: int | None = None
    web_count: int = 0
    item_count: int = 0
    last_modified: Any | None = None
    lock_state: str | None = None
    report_impacted_only: bool = False
