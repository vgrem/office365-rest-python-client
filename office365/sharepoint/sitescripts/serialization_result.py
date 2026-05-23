from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


@dataclass
class SiteScriptSerializationResult(ClientValue):
    """
    :param str json:
    :param list[str] warnings:
    """

    JSON: str | None = None
    Warnings: StringCollection | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteScriptSerializationResult"
