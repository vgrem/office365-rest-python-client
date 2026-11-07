from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from office365.entity import Entity
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.queries.service_operation import ServiceOperationQuery

if TYPE_CHECKING:
    from office365.security.cases.exportfilestructure import ExportFileStructure
    from office365.security.cases.exportoptions import ExportOptions
    from office365.security.ediscovery.ediscovery_review_tag import EdiscoveryReviewTag


class EdiscoveryReviewSetQuery(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.EdiscoveryReviewSetQuery"

    def export(
        self, output_name: str, description: str, export_options: ExportOptions, export_structure: ExportFileStructure
    ) -> Self:
        """export operation.

        Args:
            output_name (str):
                outputName parameter
            description (str):
                description parameter
            export_options (ExportOptions):
                exportOptions parameter
            export_structure (ExportFileStructure):
                exportStructure parameter
        """
        qry = ServiceOperationQuery(
            self,
            "export",
            None,
            {
                "outputName": output_name,
                "description": description,
                "exportOptions": export_options,
                "exportStructure": export_structure,
            },
            None,
            None,
        )
        self.context.add_query(qry)
        return self

    def apply_tags(
        self,
        tags_to_add: ClientValueCollection[EdiscoveryReviewTag],
        tags_to_remove: ClientValueCollection[EdiscoveryReviewTag],
    ) -> Self:
        """applyTags operation.

        Args:
            tags_to_add (ClientValueCollection[EdiscoveryReviewTag]):
                tagsToAdd parameter
            tags_to_remove (ClientValueCollection[EdiscoveryReviewTag]):
                tagsToRemove parameter
        """
        qry = ServiceOperationQuery(
            self, "applyTags", None, {"tagsToAdd": tags_to_add, "tagsToRemove": tags_to_remove}, None, None
        )
        self.context.add_query(qry)
        return self
