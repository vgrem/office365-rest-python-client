from __future__ import annotations

from office365.communications.calls.transcript import CallTranscript
from office365.communications.onlinemeetings.recordings.call import CallRecording
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class AdhocCall(Entity):
    @property
    def recordings(self) -> EntityCollection[CallRecording]:
        """Gets the recordings property"""
        return self.properties.get(
            "recordings",
            EntityCollection[CallRecording](self.context, CallRecording, ResourcePath("recordings", self.resource_path)),
        )

    @property
    def transcripts(self) -> EntityCollection[CallTranscript]:
        """Gets the transcripts property"""
        return self.properties.get(
            "transcripts",
            EntityCollection[CallTranscript](
                self.context, CallTranscript, ResourcePath("transcripts", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AdhocCall"
