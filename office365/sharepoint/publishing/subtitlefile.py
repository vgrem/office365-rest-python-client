from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SubtitleFile(Entity):
    @odata(name="Language")
    @property
    def language(self) -> Optional[str]:
        """Gets the Language property"""
        return self.properties.get("Language", None)

    @odata(name="NativeLanguageName")
    @property
    def native_language_name(self) -> Optional[str]:
        """Gets the NativeLanguageName property"""
        return self.properties.get("NativeLanguageName", None)

    @odata(name="Url")
    @property
    def url(self) -> Optional[str]:
        """Gets the Url property"""
        return self.properties.get("Url", None)

    @property
    def entity_type_name(self):
        return "SP.Publishing.SubtitleFile"
