from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.working_hours import WorkingHours
from office365.outlook.locale_info import LocaleInfo
from office365.outlook.mail.automaticreplies.setting import AutomaticRepliesSetting
from office365.outlook.mail.delegatemeetingmessagedeliveryoptions import DelegateMeetingMessageDeliveryOptions
from office365.outlook.mail.userpurpose import UserPurpose
from office365.runtime.client_value import ClientValue


@dataclass
class MailboxSettings(ClientValue):
    """Settings for the primary mailbox of a user."""

    timeFormat: str | None = None
    timeZone: str | None = None
    automaticRepliesSetting: AutomaticRepliesSetting = field(default_factory=AutomaticRepliesSetting)
    archiveFolder: str | None = None
    dateFormat: str | None = None
    language: LocaleInfo = field(default_factory=LocaleInfo)
    workingHours: WorkingHours = field(default_factory=WorkingHours)
    delegateMeetingMessageDeliveryOptions: DelegateMeetingMessageDeliveryOptions | None = None
    userPurpose: UserPurpose | None = None

    @property
    def entity_type_name(self):
        return "microsoft.graph.MailboxSettings"
