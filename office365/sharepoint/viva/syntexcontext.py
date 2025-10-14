from typing import Optional

from office365.sharepoint.entity import Entity


class SyntexContext(Entity):

    @property
    def syntex_ai_builder_enabled(self) -> Optional[bool]:
        """Gets the SyntexAIBuilderEnabled property"""
        return self.properties.get("SyntexAIBuilderEnabled", None)

    @property
    def syntex_document_understanding_enabled(self) -> Optional[bool]:
        """Gets the SyntexDocumentUnderstandingEnabled property"""
        return self.properties.get("SyntexDocumentUnderstandingEnabled", None)

    @property
    def syntex_prebuilt_enabled(self) -> Optional[bool]:
        """Gets the SyntexPrebuiltEnabled property"""
        return self.properties.get("SyntexPrebuiltEnabled", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.ContentCenter.SyntexContext"
