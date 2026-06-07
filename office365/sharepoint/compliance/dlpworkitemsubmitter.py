from office365.sharepoint.entity import Entity


class ComplianceDlpWorkItemSubmitter(Entity):
    @property
    def entity_type_name(self) -> str:
        return "SP.ComplianceFoundation.ComplianceDlpWorkItemSubmitter"
