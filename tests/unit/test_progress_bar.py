"""Offline tests for the optional tqdm-backed progress hook."""

from __future__ import annotations

import builtins
import sys
import types

from office365.runtime.operations import Progress
from office365.runtime.progress import progress_bar

_TOTAL = 10
_FIRST_DONE = 3
_SECOND_DONE = 10
_ADOPTED_TOTAL = 12


def test_progress_bar_without_tqdm_is_a_noop(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "tqdm":
            raise ImportError("tqdm not installed")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    hook = progress_bar("scan")

    assert hook(Progress(done=1, total=2)) is None


def test_progress_bar_advances_a_fake_tqdm(monkeypatch):
    instances: list = []

    class FakeBar:
        def __init__(self, desc=None, total=None):
            self.desc = desc
            self.total = total
            self.n = 0
            self.updates: list[int] = []
            instances.append(self)

        def update(self, n):
            self.n += n
            self.updates.append(n)

    fake = types.ModuleType("tqdm")
    fake.tqdm = FakeBar
    monkeypatch.setitem(sys.modules, "tqdm", fake)

    hook = progress_bar("scan", total=_TOTAL)
    hook(Progress(done=_FIRST_DONE, total=_TOTAL))
    hook(Progress(done=_SECOND_DONE, total=_ADOPTED_TOTAL))

    bar = instances[0]
    assert bar.desc == "scan"
    assert bar.updates == [_FIRST_DONE, _SECOND_DONE - _FIRST_DONE]
    assert bar.n == _SECOND_DONE
    assert bar.total == _ADOPTED_TOTAL
