"""Optional tqdm-backed progress hook.

Long-running operations report structured
:class:`~office365.runtime.operations.Progress` snapshots to an optional
``Callable[[Progress], None]`` hook. Examples kept re-implementing the same
tqdm adapter; :func:`progress_bar` centralizes it.

``tqdm`` remains an optional dependency: when it is not installed the returned
hook is a no-op, so importing this module never requires it.
"""

from __future__ import annotations

from typing import Optional

from office365.runtime.operations import Progress, ProgressCallback


def progress_bar(description: str, *, total: Optional[int] = None) -> ProgressCallback:
    """Return a ``Callable[[Progress], None]`` that renders a tqdm progress bar.

    ``tqdm`` is optional; install it to see the bar. Without it the returned
    hook does nothing, so callers never need to guard the import.

    Args:
        description: Label shown next to the bar.
        total: Optional total when known upfront. When omitted, the bar adopts
            the total from the first :class:`Progress` snapshot that carries one.

    Returns:
        A progress hook suitable for the ``progress=`` argument of long-running
        operations.
    """
    try:
        from tqdm import tqdm
    except ImportError:  # pragma: no cover - exercised only without tqdm installed

        def _noop(progress: Progress) -> None:
            return None

        return _noop

    bar = tqdm(desc=description, total=total)

    def hook(progress: Progress) -> None:
        if progress.total is not None and bar.total != progress.total:
            bar.total = progress.total
        bar.update(progress.done - bar.n)
        if progress.total is not None and progress.done >= progress.total:
            bar.close()

    return hook
