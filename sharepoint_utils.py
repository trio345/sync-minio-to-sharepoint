# sharepoint_utils.py
import requests
from urllib.parse import quote
from config import GRAPH_API_BASE

def get_access_token(tenant_id, client_id, client_secret):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    r = requests.post(url, data=data)
    r.raise_for_status()
    return r.json()["access_token"]

def get_site_id(hostname, site_path, access_token):
    url = f"{GRAPH_API_BASE}/sites/{hostname}:/sites/{site_path}"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["id"]

def get_drive_id(site_id, access_token, library_name="Documents"):
    url = f"{GRAPH_API_BASE}/sites/{site_id}/drives"
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    for d in r.json().get("value", []):
        if d["name"] == library_name or d["name"] == "Shared Documents":
            return d["id"]
    raise Exception(f"Drive '{library_name}' not found")

def ensure_folder(drive_id, folder_path, access_token):
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    base_url = f"{GRAPH_API_BASE}/drives/{drive_id}/root"
    folder_path = folder_path.strip("/")

    if not folder_path:
        return None

    parent_id = None
    for segment in folder_path.split("/"):
        if parent_id is None:
            check_url = f"{base_url}:/{quote(segment)}"
        else:
            check_url = f"{GRAPH_API_BASE}/drives/{drive_id}/items/{parent_id}:/{quote(segment)}"

        r = requests.get(check_url, headers=headers)
        if r.status_code == 200:
            parent_id = r.json()["id"]
            continue

        if r.status_code == 404:
            create_url = f"{base_url}/children" if parent_id is None else f"{GRAPH_API_BASE}/drives/{drive_id}/items/{parent_id}/children"
            payload = {"name": segment, "folder": {}, "@microsoft.graph.conflictBehavior": "fail"}
            res = requests.post(create_url, headers=headers, json=payload)
            if res.status_code in (200, 201):
                parent_id = res.json()["id"]
            else:
                print(f"⚠️ Gagal membuat folder '{segment}': {res.status_code}")
                return None
    return parent_id

def upload_file(drive_id, access_token, file_path, file_data):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"{GRAPH_API_BASE}/drives/{drive_id}/root:/{file_path}:/content"
    r = requests.put(url, headers=headers, data=file_data)
    if r.status_code not in [200, 201]:
        print(f"⚠️ Gagal upload {file_path}: {r.status_code}")
        return 0
    else:
        item = r.json()
        print(f"✅ Uploaded: {file_path}")
        return item["id"]

def set_metadata(drive_id, access_token, item_id, source_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"SourceID": source_id}
    url = f"{GRAPH_API_BASE}/drives/{drive_id}/items/{item_id}/listItem/fields"
    r = requests.patch(url, headers=headers, json=data)
    r.raise_for_status()
    print(f"Metadata diset untuk file {item_id}")    

def get_all_files(drive_id, access_token, folder_path=""):
    headers = {"Authorization": f"Bearer {access_token}"}
    all_files = {}
    url = f"{GRAPH_API_BASE}/drives/{drive_id}/root:/{folder_path}:/children?expand=listItem" if folder_path else f"{GRAPH_API_BASE}/drives/{drive_id}/root/children?expand=listItem"
    while url:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        for item in data.get("value", []):
            if "file" in item:
                fields = item.get("listItem", {}).get("fields", {})
                path = item["parentReference"]["path"]
                relative_path = path.split('root:/')[-1].strip('/')
                full_path = f"{relative_path}/{item["name"]}" if relative_path else item['name']
                all_files[full_path] = {
                    "id": item["id"],
                    "size": item["size"],
                    "last_modified": item["lastModifiedDateTime"],
                    "source_id": fields.get("SourceID")
                }

            elif "folder" in item:
                subfolder = item['name']
                sub = get_all_files(drive_id, access_token, f"{folder_path}/{subfolder}".strip('/'))
                all_files.update(sub)
        url = data.get("@odata.nextLink")
    return all_files
