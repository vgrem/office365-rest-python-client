from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.search.refiner.refiner import Refiner


@dataclass
class RefinementResults(ClientValue):
    """
    The RefinementResults table contains refinement results that apply to the search query.
    """

    GroupTemplateId: str | None = None
    ItemTemplateId: str | None = None
    Refiners: ClientValueCollection[Refiner] = field(default_factory=lambda: ClientValueCollection(Refiner))
    Properties: dict | None = None
    ResultTitle: str | None = None
    ResultTitleUrl: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.Office.Server.Search.REST.RefinementResults"
