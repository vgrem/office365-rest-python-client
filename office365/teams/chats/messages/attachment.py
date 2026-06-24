from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ChatMessageAttachment(ClientValue):
    """Represents an attachment to a chat message entity.

    An entity of type chatMessageAttachment is returned as part of the Get channel messages API, as a part of
    chatMessage entity.

    Args:
        content (str): The content of the attachment. If the attachment is a rich card, set the property to
          the rich card object. This property and contentUrl are mutually exclusive.
        contentType (str): The media type of the content attachment. It can have the following values:
          reference: Attachment is a link to another file. Populate the contentURL with the link to the object.
          Any contentTypes supported by the Bot Framework's Attachment object
          application/vnd.microsoft.card.codesnippet: A code snippet. application/vnd.microsoft.card.announcement:
          An announcement header.
        contentUrl (str): URL for the content of the attachment. Supported protocols: http, https, file and data.
        name (str): Name of the attachment.
        teamsAppId (str): The ID of the Teams app that is associated with the attachment.
          The property is specifically used to attribute a Teams message card to the specified app.
        thumbnailUrl (str): URL to a thumbnail image that the channel can use if it supports using an alternative,
          smaller form of content or contentUrl. For example, if you set contentType to application/word and set
          contentUrl to the location of the Word document, you might include a thumbnail image that represents
          the document. The channel could display the thumbnail image instead of the document. When the user
          clicks the image, the channel would open the document.
    """

    id: str | None = None
    name: str | None = None
    content: str | None = None
    contentType: str | None = None
    contentUrl: str | None = None
    teamsAppId: str | None = None
    thumbnailUrl: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.ChatMessageAttachment"
