from office365.directory.rolemanagement.templates.template import DirectoryRoleTemplate
from office365.entity_collection import EntityCollection


class DirectoryRoleTemplateCollection(EntityCollection[DirectoryRoleTemplate]):
    """User's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, DirectoryRoleTemplate, resource_path)
