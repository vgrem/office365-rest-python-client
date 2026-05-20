from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class RenderListDataParameters(ClientValue):
    """Specifies the parameters to be used to render list data as a JSON string

    Fields:
        AddAllFields (bool):
        AddAllViewFields (bool):
        AddRegionalSettings (bool):
        AddRequiredFields (bool): This parameter indicates if we return required fields.
        AllowMultipleValueFilterForTaxonomyFields (bool): This parameter indicates whether multi value
            filtering is allowed for taxonomy fields.
        AudienceTarget (bool):
        DatesInUtc (bool): Specifies if the DateTime field is returned in UTC or local time.
        ExpandGroups (bool): Specifies whether to expand the grouping or not.
        ExpandUserField (bool):
        FilterOutChannelFoldersInDefaultDocLib (bool):
        RenderOptions (int): Specifies the type of output to return.
        RequireFolderColoringFields (bool):
        ShowStubFile (bool):
        ViewXml (str): Specifies the CAML view XML.
    """

    AddAllFields: Optional[bool] = None
    AddAllViewFields: Optional[bool] = None
    AddRegionalSettings: Optional[bool] = None
    AddRequiredFields: Optional[bool] = None
    AllowMultipleValueFilterForTaxonomyFields: Optional[bool] = None
    AudienceTarget: Optional[bool] = None
    DatesInUtc: Optional[bool] = None
    ExpandGroups: Optional[bool] = None
    ExpandUserField: Optional[bool] = None
    FilterOutChannelFoldersInDefaultDocLib: Optional[bool] = None
    RenderOptions: Optional[int] = None
    RequireFolderColoringFields: Optional[bool] = None
    ShowStubFile: Optional[bool] = None
    ViewXml: Optional[str] = None
    FirstGroupOnly: Optional[bool] = None
    FolderServerRelativeUrl: Optional[str] = None
    ImageFieldsToTryRewriteToCdnUrls: Optional[str] = None
    MergeDefaultView: Optional[bool] = None
    ModernListBoot: Optional[bool] = None
    OriginalDate: Optional[bool] = None
    OverrideViewXml: Optional[str] = None
    Paging: Optional[str] = None
    RenderURLFieldInJSON: Optional[bool] = None
    ReplaceGroup: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.RenderListDataParameters"
