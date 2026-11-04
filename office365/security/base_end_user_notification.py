from __future__ import annotations

from typing import TYPE_CHECKING

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value

if TYPE_CHECKING:
    from office365.security.end_user_notification import EndUserNotification


@value
class BaseEndUserNotification(ClientValue):
    defaultLanguage: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.BaseEndUserNotification"

    endUserNotification: EndUserNotification | None = None
