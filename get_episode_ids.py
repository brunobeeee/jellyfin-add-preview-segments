import requests
import uuid

def get_episode_ids(jellyfin_url, api_key, library_id):
    print("Getting episode ids...")
    headers = {
        "X-Emby-Token": api_key
    }
    params = {
        "ParentID": library_id,
        "Recursive": "true",
        "includeItemTypes": "Episode",
        "LocationTypes": "FileSystem",
        "SortBy": "SeriesSortName,PremiereDate,Name",
        "Limit": 10000
    }
    response = requests.get(f"{jellyfin_url}/Items", headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: Unable to fetch items from Jellyfin. Status code: {response.status_code}")
        return []
    data = response.json()
    items = data.get("Items", [])
    print(f"Found {len(items)} episodes.")

    # Strip IDs in UUID format and uppercase
    ids = [str(uuid.UUID(item["Id"])).upper() for item in items]
    return ids