from __future__ import annotations

from typing import Optional

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class TranslationNotificationRecipientUsers(Entity):
    @odata(name="LanguageCode")
    @property
    def language_code(self) -> Optional[str]:
        return self.properties.get("LanguageCode", None)

    @odata(name="Recipients", navigation=True)
    @property
    def recipients(self):
        from office365.sharepoint.principal.users.collection import UserCollection

        return self.properties.get(
            "Recipients",
            UserCollection(self.context, ResourcePath("Recipients", self.resource_path)),
        )
