from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.security.action import Action

if TYPE_CHECKING:
    from office365.directory.identities.provider import IdentityProvider


@value
class Account(ClientValue):
    identifier: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.Account"

    actions: ClientValueCollection[Action] = field(default_factory=lambda: ClientValueCollection(Action))

    identityProvider: IdentityProvider | None = None
