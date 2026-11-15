from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.onboarding.prioritysiterename.job import PrioritySiteRenameJob
from office365.sharepoint.onboarding.siterename.job import SiteRenameJob
from office365.sharepoint.onboarding.tenantrename.job import TenantRenameJob


class OnboardingServicesBeta(Entity):
    @odata(name="PrioritySiteRenameJobs", navigation=True)
    @property
    def priority_site_rename_jobs(self) -> EntityCollection[PrioritySiteRenameJob]:
        """Gets the PrioritySiteRenameJobs property"""
        return self.properties.get(
            "PrioritySiteRenameJobs",
            EntityCollection[PrioritySiteRenameJob](
                self.context, PrioritySiteRenameJob, ResourcePath("PrioritySiteRenameJobs", self.resource_path)
            ),
        )

    @odata(name="SiteRenameJobs", navigation=True)
    @property
    def site_rename_jobs(self) -> EntityCollection[SiteRenameJob]:
        """Gets the SiteRenameJobs property"""
        return self.properties.get(
            "SiteRenameJobs",
            EntityCollection[SiteRenameJob](
                self.context, SiteRenameJob, ResourcePath("SiteRenameJobs", self.resource_path)
            ),
        )

    @odata(name="TenantRenameJobs", navigation=True)
    @property
    def tenant_rename_jobs(self) -> EntityCollection[TenantRenameJob]:
        """Gets the TenantRenameJobs property"""
        return self.properties.get(
            "TenantRenameJobs",
            EntityCollection[TenantRenameJob](
                self.context, TenantRenameJob, ResourcePath("TenantRenameJobs", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.Onboarding.RestService.OnboardingServicesBeta"
