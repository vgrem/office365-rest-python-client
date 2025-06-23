from enum import Enum


class WebTemplateType(Enum):
    """Enum representing SharePoint web templates with their internal names and values."""

    def __str__(self):
        return self.value

    # Global/Common Templates
    GLOBAL = "GLOBAL#0"  # Global template (classic team site)
    STS = "STS#0"  # Classic team site
    STS_MODERN = "STS#3"  # Modern team site
    GROUP = "GROUP#0"  # M365 Group-connected team site

    # Publishing Templates
    BLANK_INTERNET = "BLANKINTERNET#0"  # Publishing portal
    CMS_PUBLISHING = "CMSPUBLISHING#0"  # Publishing site
    ENTERPRISE_WIKI = "ENTERWIKI#0"  # Enterprise wiki

    # Collaboration Templates
    DOCUMENT_WORKSPACE = "STS#2"  # Document workspace
    BLOG = "BLOG#0"  # Blog site
    WIKI = "WIKI#0"  # Wiki site
    PROJECT_SITE = "PROJECTSITE#0"  # Project site

    # Meeting Workspaces
    MEETING_BASIC = "MPS#0"  # Basic meeting workspace
    MEETING_BLANK = "MPS#1"  # Blank meeting workspace

    # Special Templates
    SEARCH_CENTER = "SRCHCEN#0"  # Search center
    BI_CENTER = "BICENTER#0"  # Business Intelligence Center
    DEV_SITE = "DEV#0"  # Developer site
    APP_CATALOG = "APPCATALOG#0"  # App catalog
    COMMUNICATION_SITE = "SITEPAGEPUBLISHING#0"  # Communication site

    # Custom/Add-on Templates
    COMMUNITY_SITE = "COMMUNITY#0"  # Community site
    PRODUCT_CATALOG = "PRODUCTCATALOG#0"  # Product catalog
    RECORDS_CENTER = "OFFILE#0"  # Records center
