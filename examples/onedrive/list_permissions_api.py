"""
Demonstrates @require_permission — metadata-only permission annotations.

Usage:
    >>> from office365.onedrive.drives.collection import DriveCollection
    >>> help(DriveCollection.get)
    >>> from office365.onedrive.drives.drive import Drive
    >>> help(Drive.get)
"""

from office365.onedrive.drives.collection import DriveCollection
from office365.onedrive.drives.drive import Drive

print("=" * 72)
print("help(DriveCollection.get)")
print("=" * 72)
help(DriveCollection.get)

print()
print("=" * 72)
print("help(Drive.get)")
print("=" * 72)
help(Drive.get)
