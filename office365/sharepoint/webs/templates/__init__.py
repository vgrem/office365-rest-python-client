"""SharePoint web (site) templates — the template entity, collection, and catalog."""

from office365.sharepoint.webs.templates.collection import WebTemplateCollection
from office365.sharepoint.webs.templates.template import WebTemplate
from office365.sharepoint.webs.templates.type import WebTemplateType

__all__ = [
    "WebTemplate",
    "WebTemplateCollection",
    "WebTemplateType",
]
