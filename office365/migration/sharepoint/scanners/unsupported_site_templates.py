"""Unsupported site templates scan — the SMAT ``UnsupportedSiteTemplates`` report.

A site collection created from an on-premises-only site definition (a Central
Administration site, a My Site host, a meeting workspace, an Access services
database, ...) has no Microsoft 365 equivalent, so it can't be migrated as-is.
This ``SITE``-container report lists the collections whose root web template is
in that legacy set.
"""

from __future__ import annotations

from dataclasses import dataclass

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.scanners.base import BaseScanner, ScanTarget
from office365.migration.sharepoint.scanners.summary import SiteScanSummary
from office365.sharepoint.webs.templates import WebTemplateType

#: Templates with no Microsoft 365 equivalent — a collection built from one can't
#: be migrated as-is. Held as template names (the part before ``#``) so the match
#: is independent of the site-definition configuration id.
_UNSUPPORTED_TEMPLATES = frozenset(
    template.name_part.upper()
    for template in (
        WebTemplateType.CENTRAL_ADMIN,
        WebTemplateType.TENANT_ADMIN,
        WebTemplateType.SHAREPOINT_ONLINE_TENANT_ADMIN,
        WebTemplateType.SHARED_SERVICES_ADMINISTRATION,
        WebTemplateType.SHAREPOINT_PORTAL_SERVER_SITE,
        WebTemplateType.SHAREPOINT_PORTAL_PERSONAL_SPACE,
        WebTemplateType.PERSONALIZATION_SITE,
        WebTemplateType.MY_SITE_HOST,
        WebTemplateType.CONTENTS_AREA,
        WebTemplateType.TOPIC_AREA,
        WebTemplateType.NEWS_SITE,
        WebTemplateType.NEWS_HOME,
        WebTemplateType.SITE_DIRECTORY,
        WebTemplateType.COMMUNITY_AREA,
        WebTemplateType.COLLABORATION_PORTAL,
        WebTemplateType.REPORT_CENTER,
        WebTemplateType.PROFILES,
        WebTemplateType.ACCESS_SERVICES,
        WebTemplateType.ASSETS_WEB_DATABASE,
        WebTemplateType.CHARITABLE_CONTRIBUTIONS_WEB_DATABASE,
        WebTemplateType.CONTACTS_WEB_DATABASE,
        WebTemplateType.ISSUES_WEB_DATABASE,
        WebTemplateType.PROJECTS_WEB_DATABASE,
        WebTemplateType.DOCUMENT_CENTER,
        WebTemplateType.EXPRESS_TEAM_SITE,
        WebTemplateType.EXPRESS_HOSTED_SITE,
        WebTemplateType.MEETING_BASIC,
        WebTemplateType.MEETING_BLANK,
        WebTemplateType.MEETING_DECISION,
        WebTemplateType.MEETING_SOCIAL,
        WebTemplateType.MEETING_MULTIPAGE,
        WebTemplateType.POWERPOINT_BROADCAST,
        WebTemplateType.BUSINESS_INTELLIGENCE_CENTER,
        WebTemplateType.VISIO_PROCESS_REPOSITORY,
    )
)


@dataclass
class UnsupportedSiteTemplatesRecord:
    """One row of the SMAT ``UnsupportedSiteTemplates-detail`` report."""

    URL: str | None = None
    Template: str | None = None
    ScanID: str | None = None


class UnsupportedSiteTemplatesScanner(BaseScanner[UnsupportedSiteTemplatesRecord]):
    """SITE-container scan: reports legacy site templates with no Microsoft 365 equivalent."""

    category = "site"
    scan_name = "UnsupportedSiteTemplates"
    record_type = UnsupportedSiteTemplatesRecord

    def run(self, target: ScanTarget[SiteScanSummary], report: AssessmentReport) -> None:
        summary = target.entity
        template = summary.web_template
        if not template or template.split("#", 1)[0].upper() not in _UNSUPPORTED_TEMPLATES:
            return
        self.records.append(
            UnsupportedSiteTemplatesRecord(
                URL=summary.site_url,
                Template=template,
                ScanID=report.scan_id or None,
            )
        )
