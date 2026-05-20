from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SiteScriptMetadata(ClientValue):
    """Represents metadata about a SharePoint site script in the SharePoint framework.
    Site scripts are used to automate the provisioning of SharePoint sites by defining actions like
    applying a theme, adding lists, and configuring site settings.

    :param Optional[str] Id: unique identifier (GUID) for the site script. This is used to uniquely identify
         the script within SharePoint.
    :param Optional[str] Content: The actual JSON content of the site script. This contains the actions that
         the script will execute when applied to a SharePoint site.
    :param Optional[str] Description:
    :param Optional[bool] IsSiteScriptPackage:
    :param Optional[str] Title:
    :param Optional[int] Version:
    """

    Id: Optional[str] = None
    Content: Optional[str] = None
    Description: Optional[str] = None
    IsSiteScriptPackage: Optional[bool] = None
    Title: Optional[str] = None
    Version: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptMetadata"
