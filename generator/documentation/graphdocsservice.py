from __future__ import annotations

from generator.builders.type_builder import TypeBuilder
from generator.documentation.baseservice import BaseDocumentationService


class GraphOpenService(BaseDocumentationService):
    """Microsoft Graph Documentation Service using OpenAPI specification"""

    def build_documentation(self, type_builder: TypeBuilder):
        pass
