from enum import Enum


class WebTemplateType(Enum):
    """SharePoint web (site) templates — internal name plus configuration id.

    The value is the ``WebTemplate`` passed to ``WebCreationInformation`` (the
    ``Name#Configuration`` string returned by ``Get-SpoWebTemplate``). The catalog
    below is the union of the classic on-premises site definitions and the
    Microsoft 365 templates; the classic ones that have no Microsoft 365
    equivalent are the migration assessment's unsupported set.

    See https://techcommunity.microsoft.com/discussions/sharepointdev/sharepoint-site-templates/2093214
    """

    def __str__(self):
        return self.value

    @property
    def name_part(self) -> str:
        """The template name without the ``#configuration`` suffix (e.g. ``"STS"``)."""
        return self.value.split("#", 1)[0]

    # Global / common
    GLOBAL = "GLOBAL#0"  # Global template
    STS = "STS#0"  # Classic team site
    BLANK_SITE = "STS#1"  # Blank site
    DOCUMENT_WORKSPACE = "STS#2"  # Document workspace
    STS_MODERN = "STS#3"  # Modern team site
    GROUP = "GROUP#0"  # M365 Group-connected team site

    # Publishing
    BLANK_INTERNET = "BLANKINTERNET#0"  # Publishing site
    PRESS_RELEASES = "BLANKINTERNET#1"  # Press releases site
    PUBLISHING_WITH_WORKFLOW = "BLANKINTERNET#2"  # Publishing site with workflow
    PUBLISHING_PORTAL = "BLANKINTERNETCONTAINER#0"  # Publishing portal
    CMS_PUBLISHING = "CMSPUBLISHING#0"  # Publishing site
    ENTERPRISE_WIKI = "ENTERWIKI#0"  # Enterprise wiki

    # Collaboration
    BLOG = "BLOG#0"  # Blog site
    WIKI = "WIKI#0"  # Wiki site
    PROJECT_SITE = "PROJECTSITE#0"  # Project site
    GROUP_WORK_SITE = "SGS#0"  # Group work site
    COMMUNITY_SITE = "COMMUNITY#0"  # Community site
    COMMUNITY_AREA = "SPSCOMMU#0"  # Community area

    # Meeting workspaces
    MEETING_BASIC = "MPS#0"  # Basic meeting workspace
    MEETING_BLANK = "MPS#1"  # Blank meeting workspace
    MEETING_DECISION = "MPS#2"  # Decision meeting workspace
    MEETING_SOCIAL = "MPS#3"  # Social meeting workspace
    MEETING_MULTIPAGE = "MPS#4"  # Multipage meeting workspace

    # Search / catalog
    SEARCH_CENTER = "SRCHCEN#0"  # Enterprise search center
    BASIC_SEARCH_CENTER = "SRCHCENTERLITE#0"  # Basic search center
    FAST_SEARCH_CENTER = "SRCHCENTERFAST#0"  # FAST search center
    APP_CATALOG = "APPCATALOG#0"  # App catalog
    PRODUCT_CATALOG = "PRODUCTCATALOG#0"  # Product catalog
    DEV_SITE = "DEV#0"  # Developer site
    COMMUNICATION_SITE = "SITEPAGEPUBLISHING#0"  # Communication site

    # Records / document centers
    DOCUMENT_CENTER = "BDR#0"  # Document center
    RECORDS_CENTER = "OFFILE#0"  # Records center
    VISIO_PROCESS_REPOSITORY = "visprus#0"  # Visio process repository

    # Business intelligence / reporting
    BI_CENTER = "BICENTER#0"  # Business Intelligence Center
    BUSINESS_INTELLIGENCE_CENTER = "PPSMASite#0"  # Business Intelligence Center
    REPORT_CENTER = "SPSREPORTCENTER#0"  # Report center

    # Access services web databases
    ACCESS_SERVICES = "ACCSRV#0"  # Access services site
    ASSETS_WEB_DATABASE = "ACCSRV#1"  # Assets web database
    CHARITABLE_CONTRIBUTIONS_WEB_DATABASE = "ACCSRV#3"  # Charitable contributions web database
    CONTACTS_WEB_DATABASE = "ACCSRV#4"  # Contacts web database
    PROJECTS_WEB_DATABASE = "ACCSRV#5"  # Projects web database
    ISSUES_WEB_DATABASE = "ACCSRV#6"  # Issues web database

    # Administration / personal / legacy portals
    CENTRAL_ADMIN = "CENTRALADMIN#0"  # Central administration site
    TENANT_ADMIN = "TENANTADMIN#0"  # Tenant administration site
    SHAREPOINT_ONLINE_TENANT_ADMIN = "TenantAdminSpo#0"  # SharePoint Online tenant admin
    SHARED_SERVICES_ADMINISTRATION = "OSRV#0"  # Shared services administration site
    SHAREPOINT_PORTAL_SERVER_SITE = "SPS#0"  # SharePoint Portal Server site
    SHAREPOINT_PORTAL_PERSONAL_SPACE = "SPSPERS#0"  # SharePoint Portal Server personal space
    PERSONALIZATION_SITE = "SPSMSITE#0"  # Personalization site
    MY_SITE_HOST = "SPSMSITEHOST#0"  # My Site host
    CONTENTS_AREA = "SPSTOC#0"  # Contents area template
    TOPIC_AREA = "SPSTOPIC#0"  # Topic area template
    NEWS_SITE = "SPSNEWS#0"  # News site
    NEWS_HOME = "SPSNHOME#0"  # News home
    SITE_DIRECTORY = "SPSSITES#0"  # Site directory
    COLLABORATION_PORTAL = "SPSPORTAL#0"  # Collaboration portal
    PROFILES = "PROFILES#0"  # Profiles
    EXPRESS_TEAM_SITE = "EXPRESS#0"  # Express team site
    EXPRESS_HOSTED_SITE = "EHS#0"  # Express hosted site
    POWERPOINT_BROADCAST = "PowerPointBroadcast#0"  # PowerPoint broadcast site
