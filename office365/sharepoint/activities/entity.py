from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.activities.action_facet import ActionFacet
from office365.sharepoint.activities.facets.activity_time import ActivityTimeFacet
from office365.sharepoint.activities.facets.coalesced import CoalescedFacet
from office365.sharepoint.activities.facets.in_doc import InDocFacet
from office365.sharepoint.activities.facets.resource import ResourceFacet
from office365.sharepoint.entity import Entity
from office365.sharepoint.sharing.principal import Principal


class SPActivityEntity(Entity):
    """"""

    @odata(name="action")
    @property
    def action(self) -> ActionFacet:
        return self.properties.get("action", ActionFacet())

    @odata(name="actor")
    @property
    def actor(self) -> Principal:
        return self.properties.get("actor", Principal())

    @odata(name="isCoalesced")
    @property
    def is_coalesced(self) -> CoalescedFacet:
        return self.properties.get("isCoalesced", CoalescedFacet())

    @odata(name="docDetails")
    @property
    def doc_details(self) -> InDocFacet:
        return self.properties.get("docDetails", InDocFacet())

    @odata(name="resource")
    @property
    def resource(self) -> ResourceFacet:
        return self.properties.get("resource", ResourceFacet())

    @odata(name="times")
    @property
    def times(self) -> ActivityTimeFacet:
        return self.properties.get("times", ActivityTimeFacet())

    @property
    def property_ref_name(self):
        return "id"

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Activities.SPActivityEntity"

    def set_property(self, name, value, persist_changes=True):
        super().set_property(name, value, persist_changes)
        if name == self.property_ref_name:
            self._resource_path.set_segment(value)
        return self

    @odata(name="id")
    @property
    def id(self) -> Optional[str]:
        """Gets the id property"""
        return self.properties.get("id", None)
