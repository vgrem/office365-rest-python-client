"""Upload-session chunk limits for OneDrive and SharePoint drive items.

Source: https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession
("Upload large files with an upload session"). Byte ranges must be a multiple of
320 KiB, the recommended fragment size is 5-10 MiB, and a single request may carry
at most 60 MiB.
"""

from __future__ import annotations

UPLOAD_CHUNK_UNIT = 320 * 1024
"""Graph upload-session ranges must be a multiple of 320 KiB."""

UPLOAD_CHUNK_DEFAULT = 32 * UPLOAD_CHUNK_UNIT
"""Default upload chunk size: 10 MiB (10,485,760 bytes), top of the recommended range."""

UPLOAD_CHUNK_MAX = 60 * 1024 * 1024
"""Maximum bytes allowed in a single upload request: 60 MiB."""


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
