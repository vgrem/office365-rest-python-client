from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class ListHomeItem(ClientValue):

    color: Optional[str] = None
    icon: Optional[str] = None
    isDefaultDocumentLibrary: Optional[bool] = None
    isDocLib: Optional[bool] = None
    listId: Optional[str] = None
    listUrl: Optional[str] = None
    siteAcronym: Optional[str] = None
    siteColor: Optional[str] = None
    siteIconUrl: Optional[str] = None
    siteId: Optional[str] = None
    siteTitle: Optional[str] = None
    siteUrl: Optional[str] = None
    title: Optional[str] = None
    webId: Optional[str] = None
    webTemplateConfiguration: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ListHome.ListHomeItem"