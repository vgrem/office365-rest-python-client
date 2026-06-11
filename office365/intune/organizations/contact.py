from office365.directory.objects.collection import DirectoryObjectCollection
from office365.directory.objects.object import DirectoryObject
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class OrgContact(DirectoryObject):
    """Represents an organizational contact. Organizational contacts are managed by an organization's administrators
    and are different from personal contacts. Additionally, organizational contacts are either synchronized
    from on-premises directories or from Exchange Online, and are read-only."""

    @odata(name="directReports")
    @property
    def direct_reports(self) -> DirectoryObjectCollection:
        """
        Get a user's direct reports.
        """
        return self.properties.get(
            "directReports",
            DirectoryObjectCollection(self.context, ResourcePath("directReports", self.resource_path)),
        )

    @property
    def manager(self) -> DirectoryObject:
        """
        The user or contact that is this contact's manager.
        """
        return self.properties.get(
            "manager",
            DirectoryObject(self.context, ResourcePath("manager", self.resource_path)),
        )

    @odata(name="memberOf")
    @property
    def member_of(self) -> DirectoryObjectCollection:
        """Groups that this contact is a member of."""
        return self.properties.get(
            "memberOf",
            DirectoryObjectCollection(self.context, ResourcePath("memberOf", self.resource_path)),
        )

    @odata(name="transitiveMemberOf")
    @property
    def transitive_member_of(self) -> DirectoryObjectCollection:
        """Groups that this contact is a member of, including groups that the contact is nested under."""
        return self.properties.get(
            "transitiveMemberOf",
            DirectoryObjectCollection(self.context, ResourcePath("transitiveMemberOf", self.resource_path)),
        )
