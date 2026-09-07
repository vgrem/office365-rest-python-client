from __future__ import annotations

from dataclasses import dataclass

from office365.directory.subjectset import SubjectSet


@dataclass
class TargetApplicationOwners(SubjectSet):
    pass
