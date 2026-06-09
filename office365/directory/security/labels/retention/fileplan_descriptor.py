from office365.directory.security.authority_template import AuthorityTemplate
from office365.directory.security.category_template import CategoryTemplate
from office365.directory.security.citation_template import CitationTemplate
from office365.directory.security.department_template import DepartmentTemplate
from office365.directory.security.file_plan_reference_template import FilePlanReferenceTemplate
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath


class FilePlanDescriptor(Entity):
    """Represents a file plan descriptor for a retention label."""

    @property
    def authority_template(self) -> AuthorityTemplate:
        """Gets the authorityTemplate property"""
        return self.properties.get(
            "authorityTemplate", AuthorityTemplate(self.context, ResourcePath("authorityTemplate", self.resource_path))
        )

    @property
    def category_template(self) -> CategoryTemplate:
        """Gets the categoryTemplate property"""
        return self.properties.get(
            "categoryTemplate", CategoryTemplate(self.context, ResourcePath("categoryTemplate", self.resource_path))
        )

    @property
    def citation_template(self) -> CitationTemplate:
        """Gets the citationTemplate property"""
        return self.properties.get(
            "citationTemplate", CitationTemplate(self.context, ResourcePath("citationTemplate", self.resource_path))
        )

    @property
    def department_template(self) -> DepartmentTemplate:
        """Gets the departmentTemplate property"""
        return self.properties.get(
            "departmentTemplate",
            DepartmentTemplate(self.context, ResourcePath("departmentTemplate", self.resource_path)),
        )

    @property
    def file_plan_reference_template(self) -> FilePlanReferenceTemplate:
        """Gets the filePlanReferenceTemplate property"""
        return self.properties.get(
            "filePlanReferenceTemplate",
            FilePlanReferenceTemplate(self.context, ResourcePath("filePlanReferenceTemplate", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.FilePlanDescriptor"
