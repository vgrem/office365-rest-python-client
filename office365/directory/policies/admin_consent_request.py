from __future__ import annotations

from typing import Optional

from office365.directory.identitygovernance.accessreview.reviewer_scope import AccessReviewReviewerScope
from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.odata_property import odata


class AdminConsentRequestPolicy(Entity):
    """
    Represents the policy for enabling or disabling the Microsoft Entra admin consent workflow.
    The admin consent workflow allows users to request access for apps that they wish to use and that require admin
    authorization before users can use the apps to access organizational data.
    There is a single adminConsentRequestPolicy per tenant.
    """

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @odata(name="notifyReviewers")
    @property
    def notify_reviewers(self) -> Optional[bool]:
        """Gets the notifyReviewers property"""
        return self.properties.get("notifyReviewers", None)

    @odata(name="remindersEnabled")
    @property
    def reminders_enabled(self) -> Optional[bool]:
        """Gets the remindersEnabled property"""
        return self.properties.get("remindersEnabled", None)

    @odata(name="requestDurationInDays")
    @property
    def request_duration_in_days(self) -> Optional[int]:
        """Gets the requestDurationInDays property"""
        return self.properties.get("requestDurationInDays", None)

    @odata(name="reviewers")
    @property
    def reviewers(self) -> ClientValueCollection[AccessReviewReviewerScope]:
        """Gets the reviewers property"""
        return self.properties.get(
            "reviewers", ClientValueCollection[AccessReviewReviewerScope](AccessReviewReviewerScope)
        )

    @odata(name="version")
    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AdminConsentRequestPolicy"
