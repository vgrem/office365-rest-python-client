from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.directory.identitygovernance.accessreview.target_owners import (
        TargetOwners,
    )
    from office365.outlook.mail.email_details import EmailDetails


class OwnerlessGroupPolicy(Entity):
    @odata(name="emailInfo")
    @property
    def email_info(self) -> EmailDetails:
        """Gets the emailInfo property"""
        from office365.outlook.mail.email_details import EmailDetails

        return self.properties.get("emailInfo", EmailDetails())

    @odata(name="enabledGroupIds")
    @property
    def enabled_group_ids(self) -> StringCollection:
        """Gets the enabledGroupIds property"""
        return self.properties.get("enabledGroupIds", StringCollection())

    @odata(name="isEnabled")
    @property
    def is_enabled(self) -> Optional[bool]:
        """Gets the isEnabled property"""
        return self.properties.get("isEnabled", None)

    @odata(name="maxMembersToNotify")
    @property
    def max_members_to_notify(self) -> Optional[int]:
        """Gets the maxMembersToNotify property"""
        return self.properties.get("maxMembersToNotify", None)

    @odata(name="notificationDurationInWeeks")
    @property
    def notification_duration_in_weeks(self) -> Optional[int]:
        """Gets the notificationDurationInWeeks property"""
        return self.properties.get("notificationDurationInWeeks", None)

    @odata(name="policyWebUrl")
    @property
    def policy_web_url(self) -> Optional[str]:
        """Gets the policyWebUrl property"""
        return self.properties.get("policyWebUrl", None)

    @odata(name="targetOwners")
    @property
    def target_owners(self) -> TargetOwners:
        """Gets the targetOwners property"""
        from office365.directory.identitygovernance.accessreview.target_owners import (
            TargetOwners,
        )

        return self.properties.get("targetOwners", TargetOwners())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OwnerlessGroupPolicy"
