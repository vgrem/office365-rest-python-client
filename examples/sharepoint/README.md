# SharePoint Examples

This directory contains examples for SharePoint REST API v1
 

###  Working with folders and files  
   - **Download** a file: [`./files/download.py`](./files/download.py)  
   - **Upload** a file: [`./files/upload.py`](./files/upload.py)  
   - **Create** a folder: [`./folders/create.py`](./folders/create.py)
   - **Upload** large file: [`./files/upload_large.py`](./files/upload_large.py) 
   - **List** file version history: [`./versions/list.py`](./files/versions/list.py)

###  Working with lists and list items  
   - **Create** a list item: [`/lists/create_item.py`](./lists/create_item.py)   
   - **Read** list items (paged): [`/lists/read_items.py`](./lists/read_items.py)
   - **Update** items in batch: [`./listitems/update_batch.py`](./listitems/update_batch.py)  
   - **Delete** an list item: [`./listitems/delete.py`](./listitems/delete.py)

###   Working with fields and field values  
   - **Create** lookup field: [`create_lookup.py`](./fields/create_lookup.py)  
   
###   Working with taxonomy  
   - **Get** field value : [`get_field_value.py`](./taxonomy/get_field_value.py)  
   
###   Working with site  

###  Authentication using browser session cookies
- **Authenticate with cookies**: [`../auth_cookies.py`](../auth_cookies.py)
  - Demonstrates loading `FedAuth`, `rtFa`, `SPOIDCRL` from Playwright `storage_state.json` and using `ClientContext.with_cookies(...)`.
  - Optional `ttl_seconds` parameter can periodically refresh cookies from the source.
- **Capture cookies with Playwright (optional)**: [`./auth/capture_cookies_with_playwright.py`](./auth/capture_cookies_with_playwright.py)
  - Not a library dependency. Requires `pip install playwright` and `playwright install chromium`.
  - Launches a browser to log in, then saves `storage_state.json` which can be consumed by the cookie auth example.

---

