from office365.directory.identitygovernance.appconsent.approval_stage import ApprovalStage
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class Approval(Entity):
    """Represents the approval object for decisions associated with a request.

    In PIM for groups, the approval object for decisions to approve or deny requests to activate
    group membership or ownership."""

    @property
    def stages(self) -> EntityCollection[ApprovalStage]:
        """Gets the stages property"""
        return self.properties.get(
            "stages",
            EntityCollection[ApprovalStage](self.context, ApprovalStage, ResourcePath("stages", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Approval"
