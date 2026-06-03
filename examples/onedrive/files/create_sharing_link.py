"""
Create a sharing link for a DriveItem

The following example requests a sharing link to be created for the DriveItem in the user's OneDrive.
The sharing link is configured to be read-only and usable by anyone with the link.
All existing permissions are removed when sharing for the first time if retainInheritedPermissions is false.

https://learn.microsoft.com/en-us/graph/api/driveitem-createlink?view=graph-rest-1.0
https://learn.microsoft.com/en-us/graph/api/resources/drive


Requires delegated permission ``Files.ReadWrite.All``.
"""