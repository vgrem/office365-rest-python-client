from __future__ import annotations

from office365.directory.identitygovernance.entitlementmanagement.custom_extension_behavior_on_error import (
    CustomExtensionBehaviorOnError,
)
from office365.runtime.types.value import value


@value
class FallbackToMicrosoftProviderOnError(CustomExtensionBehaviorOnError):
    pass
