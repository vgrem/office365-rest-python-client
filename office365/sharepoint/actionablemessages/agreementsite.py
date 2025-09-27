from datetime import datetime

from office365.runtime.client_value import ClientValue
from office365.sharepoint.sharepointids import SharePointIds
from office365.sharepoint.sites.template import SiteTemplate
from office365.sharepoint.viva.resourcevisualization import ResourceVisualization


class SPAgreementsSite(ClientValue):

    def __init__(
        self,
        created_date_time: datetime = datetime.min,
        description: str = None,
        group_id: str = None,
        last_modified_date_time: datetime = datetime.min,
        resource_visualization: ResourceVisualization = ResourceVisualization(),
        share_point_ids: SharePointIds = SharePointIds(),
        template: SiteTemplate = SiteTemplate(),
        title: str = None,
        web_url: str = None,
    ):
        self.CreatedDateTime = created_date_time
        self.Description = description
        self.GroupId = group_id
        self.LastModifiedDateTime = last_modified_date_time
        self.ResourceVisualization = resource_visualization
        self.SharePointIds = share_point_ids
        self.Template = template
        self.Title = title
        self.WebUrl = web_url
