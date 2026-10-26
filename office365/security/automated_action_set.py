from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.account_object_id_action import AccountObjectIdAction
from office365.security.account_sid_action import AccountSidAction
from office365.security.device_action import DeviceAction
from office365.security.email_action import EmailAction
from office365.security.file_action import FileAction
from office365.security.isolate_device_action import IsolateDeviceAction
from office365.security.stop_and_quarantine_file_action import StopAndQuarantineFileAction


@dataclass
class AutomatedActionSet(ClientValue):
    allowFiles: ClientValueCollection[FileAction] = field(default_factory=lambda: ClientValueCollection(FileAction))
    blockFiles: ClientValueCollection[FileAction] = field(default_factory=lambda: ClientValueCollection(FileAction))
    collectInvestigationPackages: ClientValueCollection[DeviceAction] = field(
        default_factory=lambda: ClientValueCollection(DeviceAction)
    )
    disableUsers: ClientValueCollection[AccountSidAction] = field(
        default_factory=lambda: ClientValueCollection(AccountSidAction)
    )
    forceUserPasswordResets: ClientValueCollection[AccountSidAction] = field(
        default_factory=lambda: ClientValueCollection(AccountSidAction)
    )
    hardDeleteEmails: ClientValueCollection[EmailAction] = field(
        default_factory=lambda: ClientValueCollection(EmailAction)
    )
    initiateInvestigations: ClientValueCollection[DeviceAction] = field(
        default_factory=lambda: ClientValueCollection(DeviceAction)
    )
    isolateDevices: ClientValueCollection[IsolateDeviceAction] = field(
        default_factory=lambda: ClientValueCollection(IsolateDeviceAction)
    )
    markUsersAsCompromised: ClientValueCollection[AccountObjectIdAction] = field(
        default_factory=lambda: ClientValueCollection(AccountObjectIdAction)
    )
    moveEmailsToDeletedItems: ClientValueCollection[EmailAction] = field(
        default_factory=lambda: ClientValueCollection(EmailAction)
    )
    moveEmailsToInbox: ClientValueCollection[EmailAction] = field(
        default_factory=lambda: ClientValueCollection(EmailAction)
    )
    moveEmailsToJunk: ClientValueCollection[EmailAction] = field(
        default_factory=lambda: ClientValueCollection(EmailAction)
    )
    restrictAppExecutions: ClientValueCollection[DeviceAction] = field(
        default_factory=lambda: ClientValueCollection(DeviceAction)
    )
    runAntivirusScans: ClientValueCollection[DeviceAction] = field(
        default_factory=lambda: ClientValueCollection(DeviceAction)
    )
    softDeleteEmails: ClientValueCollection[EmailAction] = field(
        default_factory=lambda: ClientValueCollection(EmailAction)
    )
    stopAndQuarantineFiles: ClientValueCollection[StopAndQuarantineFileAction] = field(
        default_factory=lambda: ClientValueCollection(StopAndQuarantineFileAction)
    )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AutomatedActionSet"
