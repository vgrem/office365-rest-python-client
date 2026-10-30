from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class Windows10SecureAssessmentConfiguration(Entity):
    @odata(name="allowPrinting")
    @property
    def allow_printing(self) -> Optional[bool]:
        """Gets the allowPrinting property"""
        return self.properties.get("allowPrinting", None)

    @odata(name="allowScreenCapture")
    @property
    def allow_screen_capture(self) -> Optional[bool]:
        """Gets the allowScreenCapture property"""
        return self.properties.get("allowScreenCapture", None)

    @odata(name="allowTextSuggestion")
    @property
    def allow_text_suggestion(self) -> Optional[bool]:
        """Gets the allowTextSuggestion property"""
        return self.properties.get("allowTextSuggestion", None)

    @odata(name="configurationAccount")
    @property
    def configuration_account(self) -> Optional[str]:
        """Gets the configurationAccount property"""
        return self.properties.get("configurationAccount", None)

    @odata(name="launchUri")
    @property
    def launch_uri(self) -> Optional[str]:
        """Gets the launchUri property"""
        return self.properties.get("launchUri", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Windows10SecureAssessmentConfiguration"
