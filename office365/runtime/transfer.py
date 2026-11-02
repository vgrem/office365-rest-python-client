"""Upload-session chunk arithmetic, shared by every Graph upload session.

A Graph upload session accepts a file as a sequence of byte ranges, and the service
constrains those ranges: a range must be a positive multiple of 320 KiB, the
recommended fragment is 5-10 MiB, and one request may carry at most 60 MiB. The rule
is the service's, not the product's, so it lives once here and every session -
:meth:`DriveItem.resumable_upload`, :meth:`AttachmentCollection.resumable_upload`,
:meth:`Task.upload_attachment` - reads it instead of carrying its own number.

Only the *chunk* is arithmetic. The size at which a small file is posted in one request
instead of through a session is a per-endpoint policy, and it is **not** required to be a
multiple of the unit; the two attachment collections that make that decision - a mail
attachment and a To Do task attachment - share the same published bound, so it is declared
once here too.

Source: https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession
("Upload large files with an upload session").
"""

from __future__ import annotations

UPLOAD_CHUNK_UNIT = 320 * 1024
"""Graph upload-session ranges must be a multiple of 320 KiB."""

UPLOAD_CHUNK_DEFAULT = 32 * UPLOAD_CHUNK_UNIT
"""Default upload chunk size: 10 MiB (10,485,760 bytes), top of the recommended range."""

UPLOAD_CHUNK_MAX = 60 * 1024 * 1024
"""Maximum bytes allowed in a single upload request: 60 MiB."""

INLINE_ATTACHMENT_MAX = 3 * 1024 * 1024
"""Largest attachment a mail message or a To Do task accepts in one request: 3 MiB.

Above it the attachment has to go through an upload session, which is where the chunk rule
above starts to apply. This is a *size threshold*, not a fragment size: it need not be a
multiple of :data:`UPLOAD_CHUNK_UNIT`.
"""


def check_chunk_size(chunk_size: int) -> None:
    """Validate an upload chunk size.

    Raises:
        ValueError: If ``chunk_size`` is not a positive multiple of 320 KiB or exceeds 60 MiB.
    """
    if chunk_size <= 0 or chunk_size % UPLOAD_CHUNK_UNIT:
        raise ValueError(
            f"chunk_size must be a positive multiple of 320 KiB ({UPLOAD_CHUNK_UNIT:,} bytes), got {chunk_size:,}"
        )
    if chunk_size > UPLOAD_CHUNK_MAX:
        raise ValueError(f"chunk_size must be at most 60 MiB ({UPLOAD_CHUNK_MAX:,} bytes), got {chunk_size:,}")
