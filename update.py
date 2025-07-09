import requests
import json
from math import atan, exp, pi, degrees
from datetime import datetime
from zoneinfo import ZoneInfo

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

def save_json(cameras):
    eastern = ZoneInfo("America/New_York")
    now_et = datetime.now(eastern)
    timestamp = now_et.strftime("%Y-%m-%d %H:%M %Z")

    output = {
        "_comment": f"Last updated {timestamp}",
        "cameras": cameras
    }

    with open("cameras.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    data = fetch_camera_data()
    save_json(data)
    print(f"Saved {len(data)} cameras to cameras.json")
