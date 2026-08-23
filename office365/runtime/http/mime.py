from __future__ import annotations

import mimetypes


def get_mime_type(file_name: str) -> tuple[str | None, str | None]:
    """Guess the MIME type and encoding for a filename.

    Returns:
        Tuple of (type, encoding) where either may be None
    """
    return mimetypes.guess_type(file_name)
