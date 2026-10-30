from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SyntexContext(Entity):
    @odata(name="SyntexAIBuilderEnabled", beta=True)
    @property
    def syntex_ai_builder_enabled(self) -> Optional[bool]:
        """Gets the SyntexAIBuilderEnabled property"""
        return self.properties.get("SyntexAIBuilderEnabled", None)

    @odata(name="SyntexDocumentUnderstandingEnabled", beta=True)
    @property
    def syntex_document_understanding_enabled(self) -> Optional[bool]:
        """Gets the SyntexDocumentUnderstandingEnabled property"""
        return self.properties.get("SyntexDocumentUnderstandingEnabled", None)

    @odata(name="SyntexPrebuiltEnabled", beta=True)
    @property
    def syntex_prebuilt_enabled(self) -> Optional[bool]:
        """Gets the SyntexPrebuiltEnabled property"""
        return self.properties.get("SyntexPrebuiltEnabled", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SyntexContext"
