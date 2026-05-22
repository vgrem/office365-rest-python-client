from __future__ import annotations

from dataclasses import dataclass, field

from office365.directory.policies.conditionalaccess.conditional_access import ConditionalAccessPolicy
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class AuthenticationStrengthUsage(ClientValue):
    """
    An object containing two collections of Conditional Access policies that reference the specified authentication
    strength. One collection references Conditional Access policies that require an MFA claim; the other collection
    references Conditional Access policies that don't require such a claim.
    """

    mfa: ClientValueCollection[ConditionalAccessPolicy] = field(
        default_factory=lambda: ClientValueCollection(ConditionalAccessPolicy)
    )
    none: ClientValueCollection[ConditionalAccessPolicy] = field(
        default_factory=lambda: ClientValueCollection(ConditionalAccessPolicy)
    )
