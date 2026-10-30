from __future__ import annotations

from typing import Optional

from office365.directory.permissions.email_identity import EmailIdentity
from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class EndUserNotificationDetail(Entity):
    @odata(name="emailContent")
    @property
    def email_content(self) -> Optional[str]:
        """Gets the emailContent property"""
        return self.properties.get("emailContent", None)

    @odata(name="isDefaultLangauge")
    @property
    def is_default_langauge(self) -> Optional[bool]:
        """Gets the isDefaultLangauge property"""
        return self.properties.get("isDefaultLangauge", None)

    @odata(name="language")
    @property
    def language(self) -> Optional[str]:
        """Gets the language property"""
        return self.properties.get("language", None)

    @odata(name="locale")
    @property
    def locale(self) -> Optional[str]:
        """Gets the locale property"""
        return self.properties.get("locale", None)

    @odata(name="sentFrom")
    @property
    def sent_from(self) -> EmailIdentity:
        """Gets the sentFrom property"""
        return self.properties.get("sentFrom", EmailIdentity())

    @odata(name="subject")
    @property
    def subject(self) -> Optional[str]:
        """Gets the subject property"""
        return self.properties.get("subject", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.EndUserNotificationDetail"
