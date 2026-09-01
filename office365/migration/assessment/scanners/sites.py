"""Site/web-level scanner — inventory and site-wide concerns.

The web-tree inventory lives in the assessor; this scanner is the hook-based
extension point for site-wide checks (storage/quota, features, navigation).
"""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner


class WebScanner(BaseScanner):
    """Site-collection inventory: counts the web tree (direct subsites)."""

    category = "site"

    def on_webs(self, webs, report: AssessmentReport) -> None:
        report.total_webs = len(webs)
