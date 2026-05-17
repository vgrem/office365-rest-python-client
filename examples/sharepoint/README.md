# SharePoint Examples

This directory contains examples for SharePoint REST API v1.

### Working with sites and webs
- **Get web properties**: [`webs/get_props.py`](./webs/get_props.py)
- **Get all webs**: [`webs/get_all.py`](./webs/get_all.py)
- **Get changes**: [`webs/get_changes.py`](./webs/get_changes.py)
- **Create communication site**: [`sites/create_comm.py`](./sites/create_comm.py)
- **Create team site**: [`sites/create_team.py`](./sites/create_team.py)

### Working with folders and files
- **Download a file**: [`files/download.py`](./files/download.py)
- **Upload a file**: [`files/upload.py`](./files/upload.py)
- **Upload large file**: [`files/upload_large.py`](./files/upload_large.py)
- **Create a folder**: [`folders/create.py`](./folders/create.py)
- **Delete a folder**: [`folders/delete.py`](./folders/delete.py)
- **Move a file**: [`files/move_file.py`](./files/move_file.py)
- **Copy a folder**: [`folders/copy_folder.py`](./folders/copy_folder.py)
- **List file version history**: [`files/versions/list.py`](./files/versions/list.py)

### Working with lists and list items
- **Create a list**: [`lists/create.py`](./lists/create.py)
- **Read list items (paged)**: [`lists/read_paged.py`](./lists/read_paged.py)
- **Read all list items**: [`lists/read_all.py`](./lists/read_all.py)
- **Create a list item**: [`listitems/create.py`](./listitems/create.py)
- **Update items in batch**: [`listitems/update_batch.py`](./listitems/update_batch.py)
- **Delete a list item**: [`listitems/delete.py`](./listitems/delete.py)
- **Filter items**: [`listitems/filter.py`](./listitems/filter.py)

### Working with fields
- **Create lookup field**: [`fields/create_lookup.py`](./fields/create_lookup.py)
- **Create date field**: [`fields/create_date.py`](./fields/create_date.py)
- **Create choice field**: [`fields/create_choice.py`](./fields/create_choice.py)
- **Create taxonomy field**: [`fields/create_taxonomy.py`](./fields/create_taxonomy.py)

### Working with permissions
- **Get permissions for list**: [`permissions/get_for_list.py`](./permissions/get_for_list.py)
- **Grant permissions to web**: [`permissions/grant_to_web.py`](./permissions/grant_to_web.py)
- **Revoke permissions**: [`permissions/revoke_from_web.py`](./permissions/revoke_from_web.py)

### Working with taxonomy
- **Get field value**: [`taxonomy/get_field_value.py`](./taxonomy/get_field_value.py)
- **Create taxonomy field**: [`taxonomy/create_field.py`](./taxonomy/create_field.py)
- **Get term set**: [`taxonomy/get_term_set.py`](./taxonomy/get_term_set.py)

### Working with search
- **Search sites**: [`search/search_sites.py`](./search/search_sites.py)
- **Search with sorting**: [`search/search_sort_list.py`](./search/search_sort_list.py)

### Working with sharing
- **Share a file**: [`sharing/share_file_org.py`](./sharing/share_file_org.py)
- **Share a folder**: [`sharing/share_folder.py`](./sharing/share_folder.py)
- **Create anonymous link**: [`sharing/create_anon_link.py`](./sharing/create_anon_link.py)

### Working with tenant administration
- **Get all site collections**: [`tenant/get_all_sites.py`](./tenant/get_all_sites.py)
- **Set site admin**: [`tenant/set_site_admin.py`](./tenant/set_site_admin.py)
- **Delete sites**: [`tenant/delete_sites.py`](./tenant/delete_sites.py)
- **Export tenant settings**: [`tenant/export_tenant_settings.py`](./tenant/export_tenant_settings.py)

### Working with users and groups
- **Get current user**: [`users/whoami.py`](./users/whoami.py)
- **List site users**: [`users/list_site_users.py`](./users/list_site_users.py)
- **Add user to web**: [`users/add_to_web.py`](./users/add_to_web.py)
- **Manage groups**: [`groups/add_remove.py`](./groups/add_remove.py)

### Authentication examples
- **Modern auth methods**: [`auth/modern/`](./auth/modern/)
- **Legacy auth methods**: [`auth/legacy/`](./auth/legacy/)
