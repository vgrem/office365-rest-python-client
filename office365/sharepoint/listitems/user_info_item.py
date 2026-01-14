from datetime import datetime
from typing import Optional
from uuid import UUID

from office365.sharepoint.fields.url_value import FieldUrlValue
from office365.sharepoint.listitems.listitem import ListItem


class UserInfoItem(ListItem):
    @property
    def content_type_id(self) -> Optional[str]:
        """Gets the ContentTypeId property"""
        return self.properties.get("ContentTypeId", None)

    @property
    def title(self) -> Optional[str]:
        """Gets the Title property"""
        return self.properties.get("Title", None)

    @property
    def o_data___moderation_comments(self) -> Optional[str]:
        """Gets the OData__ModerationComments property"""
        return self.properties.get("OData__ModerationComments", None)

    @property
    def file_x0020__type(self) -> Optional[str]:
        """Gets the File_x0020_Type property"""
        return self.properties.get("File_x0020_Type", None)

    @property
    def compliance_asset_id(self) -> Optional[str]:
        """Gets the ComplianceAssetId property"""
        return self.properties.get("ComplianceAssetId", None)

    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def e_mail(self) -> Optional[str]:
        """Gets the EMail property"""
        return self.properties.get("EMail", None)

    @property
    def other_mail(self) -> Optional[str]:
        """Gets the OtherMail property"""
        return self.properties.get("OtherMail", None)

    @property
    def user_expiration(self) -> datetime:
        """Gets the UserExpiration property"""
        return self.properties.get("UserExpiration", datetime.min)

    @property
    def user_last_deletion_time(self) -> datetime:
        """Gets the UserLastDeletionTime property"""
        return self.properties.get("UserLastDeletionTime", datetime.min)

    @property
    def mobile_phone(self) -> Optional[str]:
        """Gets the MobilePhone property"""
        return self.properties.get("MobilePhone", None)

    @property
    def notes(self) -> Optional[str]:
        """Gets the Notes property"""
        return self.properties.get("Notes", None)

    @property
    def sip_address(self) -> Optional[str]:
        """Gets the SipAddress property"""
        return self.properties.get("SipAddress", None)

    @property
    def locale(self) -> Optional[int]:
        """Gets the Locale property"""
        return self.properties.get("Locale", None)

    @property
    def calendar_type(self) -> Optional[int]:
        """Gets the CalendarType property"""
        return self.properties.get("CalendarType", None)

    @property
    def adjust_hijri_days(self) -> Optional[int]:
        """Gets the AdjustHijriDays property"""
        return self.properties.get("AdjustHijriDays", None)

    @property
    def time_zone(self) -> Optional[int]:
        """Gets the TimeZone property"""
        return self.properties.get("TimeZone", None)

    @property
    def time24(self) -> Optional[bool]:
        """Gets the Time24 property"""
        return self.properties.get("Time24", None)

    @property
    def alt_calendar_type(self) -> Optional[int]:
        """Gets the AltCalendarType property"""
        return self.properties.get("AltCalendarType", None)

    @property
    def calendar_view_options(self) -> Optional[int]:
        """Gets the CalendarViewOptions property"""
        return self.properties.get("CalendarViewOptions", None)

    @property
    def work_days(self) -> Optional[int]:
        """Gets the WorkDays property"""
        return self.properties.get("WorkDays", None)

    @property
    def work_day_start_hour(self) -> Optional[int]:
        """Gets the WorkDayStartHour property"""
        return self.properties.get("WorkDayStartHour", None)

    @property
    def work_day_end_hour(self) -> Optional[int]:
        """Gets the WorkDayEndHour property"""
        return self.properties.get("WorkDayEndHour", None)

    @property
    def mui_languages(self) -> Optional[str]:
        """Gets the MUILanguages property"""
        return self.properties.get("MUILanguages", None)

    @property
    def content_languages(self) -> Optional[str]:
        """Gets the ContentLanguages property"""
        return self.properties.get("ContentLanguages", None)

    @property
    def is_site_admin(self) -> Optional[bool]:
        """Gets the IsSiteAdmin property"""
        return self.properties.get("IsSiteAdmin", None)

    @property
    def deleted(self) -> Optional[bool]:
        """Gets the Deleted property"""
        return self.properties.get("Deleted", None)

    @property
    def user_info_hidden(self) -> Optional[bool]:
        """Gets the UserInfoHidden property"""
        return self.properties.get("UserInfoHidden", None)

    @property
    def picture(self) -> FieldUrlValue:
        """Gets the Picture property"""
        return self.properties.get("Picture", FieldUrlValue())

    @property
    def department(self) -> Optional[str]:
        """Gets the Department property"""
        return self.properties.get("Department", None)

    @property
    def job_title(self) -> Optional[str]:
        """Gets the JobTitle property"""
        return self.properties.get("JobTitle", None)

    @property
    def is_active(self) -> Optional[bool]:
        """Gets the IsActive property"""
        return self.properties.get("IsActive", None)

    @property
    def first_name(self) -> Optional[str]:
        """Gets the FirstName property"""
        return self.properties.get("FirstName", None)

    @property
    def last_name(self) -> Optional[str]:
        """Gets the LastName property"""
        return self.properties.get("LastName", None)

    @property
    def link_title(self) -> Optional[str]:
        """Gets the LinkTitle property"""
        return self.properties.get("LinkTitle", None)

    @property
    def link_title2(self) -> Optional[str]:
        """Gets the LinkTitle2 property"""
        return self.properties.get("LinkTitle2", None)

    @property
    def work_phone(self) -> Optional[str]:
        """Gets the WorkPhone property"""
        return self.properties.get("WorkPhone", None)

    @property
    def user_name(self) -> Optional[str]:
        """Gets the UserName property"""
        return self.properties.get("UserName", None)

    @property
    def web_site(self) -> FieldUrlValue:
        """Gets the WebSite property"""
        return self.properties.get("WebSite", FieldUrlValue())

    @property
    def sps_responsibility(self) -> Optional[str]:
        """Gets the SPSResponsibility property"""
        return self.properties.get("SPSResponsibility", None)

    @property
    def office(self) -> Optional[str]:
        """Gets the Office property"""
        return self.properties.get("Office", None)

    @property
    def sps_picture_timestamp(self) -> Optional[str]:
        """Gets the SPSPictureTimestamp property"""
        return self.properties.get("SPSPictureTimestamp", None)

    @property
    def sps_picture_placeholder_state(self) -> Optional[int]:
        """Gets the SPSPicturePlaceholderState property"""
        return self.properties.get("SPSPicturePlaceholderState", None)

    @property
    def sps_picture_exchange_sync_state(self) -> Optional[int]:
        """Gets the SPSPictureExchangeSyncState property"""
        return self.properties.get("SPSPictureExchangeSyncState", None)

    @property
    def o_data___color_hex(self) -> Optional[str]:
        """Gets the OData__ColorHex property"""
        return self.properties.get("OData__ColorHex", None)

    @property
    def o_data___color_tag(self) -> Optional[str]:
        """Gets the OData__ColorTag property"""
        return self.properties.get("OData__ColorTag", None)

    @property
    def o_data___emoji(self) -> Optional[str]:
        """Gets the OData__Emoji property"""
        return self.properties.get("OData__Emoji", None)

    @property
    def modified(self) -> datetime:
        """Gets the Modified property"""
        return self.properties.get("Modified", datetime.min)

    @property
    def id_(self) -> Optional[int]:
        """Gets the ID property"""
        return self.properties.get("ID", None)

    @property
    def created(self) -> datetime:
        """Gets the Created property"""
        return self.properties.get("Created", datetime.min)

    @property
    def author_id(self) -> Optional[int]:
        """Gets the AuthorId property"""
        return self.properties.get("AuthorId", None)

    @property
    def editor_id(self) -> Optional[int]:
        """Gets the EditorId property"""
        return self.properties.get("EditorId", None)

    @property
    def o_data___has_copy_destinations(self) -> Optional[bool]:
        """Gets the OData__HasCopyDestinations property"""
        return self.properties.get("OData__HasCopyDestinations", None)

    @property
    def o_data___copy_source(self) -> Optional[str]:
        """Gets the OData__CopySource property"""
        return self.properties.get("OData__CopySource", None)

    @property
    def owshiddenversion(self) -> Optional[int]:
        """Gets the owshiddenversion property"""
        return self.properties.get("owshiddenversion", None)

    @property
    def workflow_version(self) -> Optional[int]:
        """Gets the WorkflowVersion property"""
        return self.properties.get("WorkflowVersion", None)

    @property
    def o_data__ui_version(self) -> Optional[int]:
        """Gets the OData__UIVersion property"""
        return self.properties.get("OData__UIVersion", None)

    @property
    def o_data__ui_version_string(self) -> Optional[str]:
        """Gets the OData__UIVersionString property"""
        return self.properties.get("OData__UIVersionString", None)

    @property
    def attachments(self) -> Optional[bool]:
        """Gets the Attachments property"""
        return self.properties.get("Attachments", None)

    @property
    def o_data___moderation_status(self) -> Optional[int]:
        """Gets the OData__ModerationStatus property"""
        return self.properties.get("OData__ModerationStatus", None)

    @property
    def edit(self) -> Optional[str]:
        """Gets the Edit property"""
        return self.properties.get("Edit", None)

    @property
    def link_title_no_menu(self) -> Optional[str]:
        """Gets the LinkTitleNoMenu property"""
        return self.properties.get("LinkTitleNoMenu", None)

    @property
    def select_title(self) -> Optional[str]:
        """Gets the SelectTitle property"""
        return self.properties.get("SelectTitle", None)

    @property
    def instance_id(self) -> Optional[int]:
        """Gets the InstanceID property"""
        return self.properties.get("InstanceID", None)

    @property
    def order(self) -> Optional[float]:
        """Gets the Order property"""
        return self.properties.get("Order", None)

    @property
    def guid(self) -> Optional[UUID]:
        """Gets the GUID property"""
        return self.properties.get("GUID", None)

    @property
    def workflow_instance_id(self) -> Optional[UUID]:
        """Gets the WorkflowInstanceID property"""
        return self.properties.get("WorkflowInstanceID", None)

    @property
    def file_ref(self) -> Optional[str]:
        """Gets the FileRef property"""
        return self.properties.get("FileRef", None)

    @property
    def file_dir_ref(self) -> Optional[str]:
        """Gets the FileDirRef property"""
        return self.properties.get("FileDirRef", None)

    @property
    def last_x0020__modified(self) -> datetime:
        """Gets the Last_x0020_Modified property"""
        return self.properties.get("Last_x0020_Modified", datetime.min)

    @property
    def created_x0020__date(self) -> datetime:
        """Gets the Created_x0020_Date property"""
        return self.properties.get("Created_x0020_Date", datetime.min)

    @property
    def fs_obj_type(self) -> Optional[int]:
        """Gets the FSObjType property"""
        return self.properties.get("FSObjType", None)

    @property
    def perm_mask(self) -> Optional[str]:
        """Gets the PermMask property"""
        return self.properties.get("PermMask", None)

    @property
    def principal_count(self) -> Optional[str]:
        """Gets the PrincipalCount property"""
        return self.properties.get("PrincipalCount", None)

    @property
    def file_leaf_ref(self) -> Optional[str]:
        """Gets the FileLeafRef property"""
        return self.properties.get("FileLeafRef", None)

    @property
    def unique_id(self) -> Optional[UUID]:
        """Gets the UniqueId property"""
        return self.properties.get("UniqueId", None)

    @property
    def html_x0020__file_x0020__type(self) -> Optional[str]:
        """Gets the HTML_x0020_File_x0020_Type property"""
        return self.properties.get("HTML_x0020_File_x0020_Type", None)

    @property
    def o_data___edit_menu_table_start(self) -> Optional[str]:
        """Gets the OData__EditMenuTableStart property"""
        return self.properties.get("OData__EditMenuTableStart", None)

    @property
    def o_data___edit_menu_table_start2(self) -> Optional[str]:
        """Gets the OData__EditMenuTableStart2 property"""
        return self.properties.get("OData__EditMenuTableStart2", None)

    @property
    def o_data___edit_menu_table_end(self) -> Optional[str]:
        """Gets the OData__EditMenuTableEnd property"""
        return self.properties.get("OData__EditMenuTableEnd", None)

    @property
    def link_filename_no_menu(self) -> Optional[str]:
        """Gets the LinkFilenameNoMenu property"""
        return self.properties.get("LinkFilenameNoMenu", None)

    @property
    def link_filename(self) -> Optional[str]:
        """Gets the LinkFilename property"""
        return self.properties.get("LinkFilename", None)

    @property
    def link_filename2(self) -> Optional[str]:
        """Gets the LinkFilename2 property"""
        return self.properties.get("LinkFilename2", None)

    @property
    def doc_icon(self) -> Optional[str]:
        """Gets the DocIcon property"""
        return self.properties.get("DocIcon", None)

    @property
    def server_url(self) -> Optional[str]:
        """Gets the ServerUrl property"""
        return self.properties.get("ServerUrl", None)

    @property
    def encoded_abs_url(self) -> Optional[str]:
        """Gets the EncodedAbsUrl property"""
        return self.properties.get("EncodedAbsUrl", None)

    @property
    def base_name(self) -> Optional[str]:
        """Gets the BaseName property"""
        return self.properties.get("BaseName", None)

    @property
    def o_data___level(self) -> Optional[int]:
        """Gets the OData__Level property"""
        return self.properties.get("OData__Level", None)

    @property
    def o_data___is_current_version(self) -> Optional[bool]:
        """Gets the OData__IsCurrentVersion property"""
        return self.properties.get("OData__IsCurrentVersion", None)

    @property
    def o_data___is_record(self) -> Optional[str]:
        """Gets the OData__IsRecord property"""
        return self.properties.get("OData__IsRecord", None)

    @property
    def main_link_settings(self) -> Optional[str]:
        """Gets the MainLinkSettings property"""
        return self.properties.get("MainLinkSettings", None)

    @property
    def app_author_id(self) -> Optional[int]:
        """Gets the AppAuthorId property"""
        return self.properties.get("AppAuthorId", None)

    @property
    def app_editor_id(self) -> Optional[int]:
        """Gets the AppEditorId property"""
        return self.properties.get("AppEditorId", None)

    @property
    def group_link(self) -> Optional[str]:
        """Gets the GroupLink property"""
        return self.properties.get("GroupLink", None)

    @property
    def group_edit(self) -> Optional[str]:
        """Gets the GroupEdit property"""
        return self.properties.get("GroupEdit", None)

    @property
    def imn_name(self) -> Optional[str]:
        """Gets the ImnName property"""
        return self.properties.get("ImnName", None)

    @property
    def picture_disp(self) -> Optional[str]:
        """Gets the PictureDisp property"""
        return self.properties.get("PictureDisp", None)

    @property
    def picture_only__size_36px(self) -> Optional[str]:
        """Gets the PictureOnly_Size_36px property"""
        return self.properties.get("PictureOnly_Size_36px", None)

    @property
    def picture_only__size_48px(self) -> Optional[str]:
        """Gets the PictureOnly_Size_48px property"""
        return self.properties.get("PictureOnly_Size_48px", None)

    @property
    def picture_only__size_72px(self) -> Optional[str]:
        """Gets the PictureOnly_Size_72px property"""
        return self.properties.get("PictureOnly_Size_72px", None)

    @property
    def name_with_picture(self) -> Optional[str]:
        """Gets the NameWithPicture property"""
        return self.properties.get("NameWithPicture", None)

    @property
    def name_with_picture_and_details(self) -> Optional[str]:
        """Gets the NameWithPictureAndDetails property"""
        return self.properties.get("NameWithPictureAndDetails", None)

    @property
    def edit_user(self) -> Optional[str]:
        """Gets the EditUser property"""
        return self.properties.get("EditUser", None)

    @property
    def user_selection(self) -> Optional[str]:
        """Gets the UserSelection property"""
        return self.properties.get("UserSelection", None)

    @property
    def content_type_disp(self) -> Optional[str]:
        """Gets the ContentTypeDisp property"""
        return self.properties.get("ContentTypeDisp", None)

    @property
    def entity_type_name(self):
        return "SP.Data.UserInfoItem"
