"""Teams migration product — export via the unified ``MigrationJob`` adapters.

from office365.migration import MigrationJob
from office365.migration.teams import TeamsArchiveSource, TeamsArchiveTarget

job = MigrationJob(TeamsArchiveSource(client, ["<team-id>"]), TeamsArchiveTarget("./backup"))
job.plan(); job.run(); job.verify()
"""

from office365.migration.teams.adapters import TeamsArchiveSource, TeamsArchiveTarget
from office365.migration.teams.models import (
    AppRecord,
    ChannelRecord,
    MemberRecord,
    TabRecord,
    TeamRecord,
    TeamsExportOptions,
)

__all__ = [
    "AppRecord",
    "ChannelRecord",
    "MemberRecord",
    "TabRecord",
    "TeamRecord",
    "TeamsArchiveSource",
    "TeamsArchiveTarget",
    "TeamsExportOptions",
]
