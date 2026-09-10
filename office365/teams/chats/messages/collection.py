from __future__ import annotations

import os
from pathlib import Path

from typing_extensions import Self

from office365.delta_collection import DeltaCollection
from office365.teams.chats.messages.body import ChatMessageBody
from office365.teams.chats.messages.message import ChatMessage


class ChatMessageCollection(DeltaCollection[ChatMessage]):
    """Chat message's collection"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, ChatMessage, resource_path)

    def add(self, content: str) -> ChatMessage:
        return super().add(body=ChatMessageBody(content=content))

    def download_hosted_contents(self, target_dir: str | os.PathLike) -> Self:
        """Download inline images (hosted contents) of the loaded messages.

        Deferred like the other export adapters — the download runs on
        ``execute_query()``::

            >>> channel.messages.get_all().download_hosted_contents("out/attachments").execute_query()

        Args:
            target_dir: Directory the files are written to (created if missing).
        """

        def _download(_) -> None:
            target = Path(target_dir)
            target.mkdir(parents=True, exist_ok=True)
            for message in self:
                for content in message.hosted_contents:
                    extension = (content.content_type or "application/octet-stream").split("/")[-1].split("+")[0]
                    name = f"{message.id}_{content.id}.{extension}"
                    (target / name).write_bytes(content.get_content().execute_query().value)

        return self.after_execute(_download)
