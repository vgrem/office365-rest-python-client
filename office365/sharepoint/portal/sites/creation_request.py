from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


class SPSiteCreationRequest(ClientValue):
    def __init__(
        self,
        title,
        url,
        owner=None,
        lcid=1033,
        web_template="SITEPAGEPUBLISHING#0",
        additional_site_feature_ids: GuidCollection = GuidCollection(),
        additional_web_feature_ids: GuidCollection = GuidCollection(),
        channel_group_id: str = None,
        classification: str = None,
        description: str = None,
        hub_site_id: str = None,
        related_group_id: str = None,
        sensitivity_label: str = None,
        sensitivity_label2: str = None,
        share_by_email_enabled: bool = None,
        site_design_id: str = None,
        teams_channel_type: int = None,
        time_zone_id: int = None,
        web_template_extension_id: str = None,
    ):
        """
        :param str title:
        :param str url:
        :param str owner:
        :param int lcid:
        :param str web_template:
        """
        super().__init__()
        self.Title = title
        self.Url = url
        self.WebTemplate = web_template
        self.Owner = owner
        self.Lcid = lcid
        self.ShareByEmailEnabled = False
        self.Classification = ""
        self.Description = ""
        self.SiteDesignId = "00000000-0000-0000-0000-000000000000"
        self.HubSiteId = "00000000-0000-0000-0000-000000000000"
        self.WebTemplateExtensionId = "00000000-0000-0000-0000-000000000000"
        self.AdditionalSiteFeatureIds = additional_site_feature_ids
        self.AdditionalWebFeatureIds = additional_web_feature_ids
        self.ChannelGroupId = channel_group_id
        self.Classification = classification
        self.Description = description
        self.HubSiteId = hub_site_id
        self.RelatedGroupId = related_group_id
        self.SensitivityLabel = sensitivity_label
        self.SensitivityLabel2 = sensitivity_label2
        self.ShareByEmailEnabled = share_by_email_enabled
        self.SiteDesignId = site_design_id
        self.TeamsChannelType = teams_channel_type
        self.TimeZoneId = time_zone_id
        self.WebTemplateExtensionId = web_template_extension_id

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.SPSiteCreationRequest"
