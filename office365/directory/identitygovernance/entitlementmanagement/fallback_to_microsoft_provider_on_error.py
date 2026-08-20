from __future__ import annotations

from dataclasses import dataclass

from office365.directory.identitygovernance.entitlementmanagement.custom_extension_behavior_on_error import (
    CustomExtensionBehaviorOnError,
)


@dataclass
class FallbackToMicrosoftProviderOnError(CustomExtensionBehaviorOnError):
    pass
