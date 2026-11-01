from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import GuidCollection


@dataclass
class CopyMigrationInfo(ClientValue):
    """The handle to a queued copy job.

    ``get_copy_job_progress`` needs this object itself: the queue URI and the encryption key
    are what the service polls with, so a job is not addressable by id alone.
    """

    #: ``Edm.Binary`` in the metadata; sent as the base64 string the service answers.
    EncryptionKey: str | None = None
    JobId: str | None = None
    #: The staging queue the job runs against, e.g. ``https://....queue.core.windows.net/...``.
    JobQueueUri: str | None = None
    SourceListItemUniqueIds: GuidCollection = field(default_factory=GuidCollection)
