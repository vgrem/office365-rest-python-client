from office365.migration.assessment.scanners.base import BaseScanner, mapped_property
from office365.sharepoint.sites.site import Site


class SiteScanner(BaseScanner[Site]):
    """ """

    @mapped_property("FeaturesCount")
    def features_count(self):
        return len(self.source.features)

    @mapped_property("UsersCount")
    def users_count(self):
        return len(self.source.root_web.site_users)

    @mapped_property("GroupsCount")
    def groups_count(self):
        return len(self.source.root_web.site_groups)

    def build_query(self):
        self.source.select(["UsageInfo", "Features/Name"]).expand(["Features"]).get()

        self.source.root_web.site_users.get()
        self.source.root_web.site_groups.get()
        return self
