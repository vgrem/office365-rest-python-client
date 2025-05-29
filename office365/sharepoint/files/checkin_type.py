class CheckinType:
    """Specifies the type of check in for a file."""

    MinorCheckIn = 0
    """Incremented as a minor version. Value=0."""

    MajorCheckIn = 1
    """Incremented as a major version. Value=1."""

    OverwriteCheckIn = 2
    """Overwrite the existing file. Value=2."""
