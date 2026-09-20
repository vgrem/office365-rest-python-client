"""SharePoint list view threshold.

SharePoint blocks queries that filter/sort on a non-indexed column and would
scan/return more than this many items, and trims some single-shot collection
loads to it. Kept in a neutral module so both the CAML guards and the typed
collections can share one value.
"""

from __future__ import annotations

LIST_VIEW_THRESHOLD = 5000  # SharePoint's default list view threshold
