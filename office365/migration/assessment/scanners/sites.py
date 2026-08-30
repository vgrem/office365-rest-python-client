"""Site/web-level scanner — inventory and site-wide concerns."""

from __future__ import annotations

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner


class WebScanner(BaseScanner):
    """Site-collection inventory: counts the web tree (direct subsites).

    Extension point for site-wide checks (storage/quota, features, navigation).
    """

    category = "site"

    def run(self, webs, report: AssessmentReport) -> None:
        report.total_webs = len(webs)
