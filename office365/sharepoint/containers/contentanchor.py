from datetime import time

from office365.runtime.client_value import ClientValue


class ContentAnchor(ClientValue):

    def __init__(self, timeline_offset: time = None):
        self.timelineOffset = timeline_offset

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Comments.ContentAnchor"
