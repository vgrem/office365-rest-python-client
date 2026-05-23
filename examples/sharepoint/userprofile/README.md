# User Profiles

Interact with SharePoint user profiles — view properties, manage followers,
explore social features, and access OneDrive URLs.

## 🔍 Explore

| What | File | Notes |
|------|------|-------|
| **Get profile properties** | [`get_properties.py`](./get_properties.py) | User metadata (department, skills, etc.) |
| **Export profiles** | [`export.py`](./export.py) | Batch-export profile data for all users |
| **Trending tags** | [`get_trending_tags.py`](./get_trending_tags.py) | Popular hash tags over the past week |
| **OneDrive URL** | [`get_onedrive_url.py`](./get_onedrive_url.py) | Get a user's OneDrive document library path |

## 👥 Follow

| What | File | Notes |
|------|------|-------|
| **Follow/unfollow user** | [`follow_user.py`](./follow_user.py) | Toggle following a user |
| **Check if following** | [`am_i_following.py`](./am_i_following.py) | Is the current user following someone? |
| **My followers** | [`get_my_followers.py`](./get_my_followers.py) | People following the current user |
| **People I follow** | [`get_people_followed_by.py`](./get_people_followed_by.py) | People the current user follows |
| **Followers of a user** | [`get_followers.py`](./get_followers.py) | People following a specific user |

---

## Official docs

- [SharePoint People REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/people-rest-api)
