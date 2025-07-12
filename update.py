import requests
import json
from math import atan, exp, pi, degrees
from datetime import datetime
from zoneinfo import ZoneInfo
import os

def mercator_to_latlon(x, y):
    lon = x * 180 / 20037508.34
    lat = degrees(atan(exp(y / 6378137.0)) * 2 - pi / 2)
    return round(lat, 6), round(lon, 6)

def fetch_camera_data():
    url = "https://services5.arcgis.com/QJebCdoMf4PF8fJP/ArcGIS/rest/services/Camera_Location/FeatureServer/0/query"
    params = {
        "where": "1=1",
        "outFields": "*",
        "outSR": "3857",
        "f": "json"
    }

    response = requests.get(url, params=params)
    data = response.json()
    features = data.get("features", [])

    cameras = []
    for f in features:
        geom = f.get("geometry")
        status = f["attributes"].get("Status")

        if status != "2A":
            continue

        if geom and "x" in geom and "y" in geom:
            lat, lon = mercator_to_latlon(geom["x"], geom["y"])
            cameras.append({
                "latitude": lat,
                "longitude": lon,
                "status": status
            })

    return sorted(cameras, key=lambda cam: (cam["latitude"], cam["longitude"]))

def load_previous_cameras():
    if not os.path.exists("cameras.json"):
        return []
    with open("cameras.json", "r") as f:
        try:
            data = json.load(f)
            return data.get("cameras", [])
        except Exception:
            return []

def count_location_changes(old, new):
    old_coords = {(c['latitude'], c['longitude']) for c in old}
    new_coords = {(c['latitude'], c['longitude']) for c in new}

    added = new_coords - old_coords
    removed = old_coords - new_coords
    changed = len(added) + len(removed)

    return changed

def save_json(cameras, changes):
    now_et = datetime.now(ZoneInfo("America/New_York"))
    timestamp = now_et.strftime("%Y-%m-%d %H:%M %Z")

    if changes == 0:
        change_note = "no location changes"
    elif changes == 1:
        change_note = "1 camera location changed"
    else:
        change_note = f"{changes} camera locations changed"

    output = {
        "_comment": f"Last updated {timestamp}, {change_note}",
        "cameras": cameras
    }

    with open("cameras.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    new_data = fetch_camera_data()

    if not new_data:
        exit(1)

    old_data = load_previous_cameras()
    changes = count_location_changes(old_data, new_data)
    save_json(new_data, changes)
    print(f"Saved {len(new_data)} cameras to cameras.json with {changes} change(s).")

