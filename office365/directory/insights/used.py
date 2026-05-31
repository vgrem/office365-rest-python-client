from office365.directory.insights.resource_reference import ResourceReference
from office365.directory.insights.usage_details import UsageDetails
from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class UsedInsight(Entity):
    """
    An insight representing documents used by a specific user. The insights returns the most relevant documents
    that a user viewed or modified. This includes documents in:
      OneDrive for Business
      SharePoint
    """

    @odata(name="lastUsed")
    @property
    def last_used(self) -> UsageDetails:
        """Information about when the item was last viewed or modified by the user."""
        return self.properties.get("lastUsed", UsageDetails())

    @odata(name="resourceReference")
    @property
    def resource_reference(self) -> ResourceReference:
        """Reference properties of the used document, such as the url and type of the document. Read-only"""
        return self.properties.get("resourceReference", ResourceReference())

    @property
    def resource(self) -> Entity:
        """Used for navigating to the item that was used. For file attachments, the type is fileAttachment.
        For linked attachments, the type is driveItem."""
        return self.properties.get(
            "resource",
            Entity(self.context, ResourcePath("resource", self.resource_path)),
        )
