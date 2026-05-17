from typing import Optional

from office365.sharepoint.contenttypes.content_type_id import ContentTypeId
from office365.sharepoint.entity import Entity
from office365.sharepoint.sharing.principal import Principal


class SharedDocumentInfo(Entity):
    """"""

    @property
    def activity(self) -> Optional[str]:
        """"""
        return self.properties.get("Activity", None)

    @property
    def author(self):
        """"""
        return self.properties.get("Author", Principal())

    @property
    def caller_stack(self) -> Optional[str]:
        """"""
        return self.properties.get("CallerStack", None)

    @property
    def color_hex(self) -> Optional[str]:
        """"""
        return self.properties.get("ColorHex", None)

    @property
    def color_tag(self) -> Optional[str]:
        """"""
        return self.properties.get("ColorTag", None)

    @property
    def content_type_id(self) -> Optional[str]:
        """"""
        return self.properties.get("ContentTypeId", ContentTypeId())

    @property
    def entity_type_name(self):
        return "SP.Sharing.SharedDocumentInfo"
