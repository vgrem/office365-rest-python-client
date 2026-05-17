from office365.directory.protection.policy.base import ProtectionPolicyBase
from office365.directory.protection.rules.drive import DriveProtectionRule
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class OneDriveForBusinessProtectionPolicy(ProtectionPolicyBase):
    """
    Contains details about protection policies applied to Microsoft 365 data in an organization.
    Protection policies are defined by the Global Admin (or the SharePoint Online Admin or Exchange Online Admin)
    and include what data to protect, when to protect it, and for what time period to retain the protected data
    for a single Microsoft 365 service.
    """

    @property
    def drive_inclusion_rules(self) -> EntityCollection[DriveProtectionRule]:
        """Contains the details of the Onedrive for Business protection rule."""
        return self.properties.get(
            "driveInclusionRules",
            EntityCollection(
                self.context,
                DriveProtectionRule,
                ResourcePath("driveInclusionRules", self.resource_path),
            ),
        )
