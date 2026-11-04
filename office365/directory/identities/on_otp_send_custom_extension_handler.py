from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from office365.directory.identitygovernance.entitlementmanagement.custom_extension_overwrite_configuration import (
    CustomExtensionOverwriteConfiguration,
)
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from office365.common.on_otp_send_custom_extension import OnOtpSendCustomExtension


@value
class OnOtpSendCustomExtensionHandler(ClientValue):
    configuration: CustomExtensionOverwriteConfiguration = field(default_factory=CustomExtensionOverwriteConfiguration)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.OnOtpSendCustomExtensionHandler"

    customExtension: OnOtpSendCustomExtension | None = None
