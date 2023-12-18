import requests
from core.keys.secrets import GOOGLE_MAPS_API_KEY


def get_polyline(lat1, lng1, lat2, lng2):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json",
        params={
            "origin": f"{lat1},{lng1}",
            "destination": f"{lat2},{lng2}",
            "mode": "driving",
            "avoidHighways": False,
            "avoidTolls": False,
            "alternatives": False,
            "key": GOOGLE_MAPS_API_KEY,
        },
    ).json()
    print(response)
    points = []
    for route in response["routes"]:
        for leg in route["legs"]:
            for step in leg["steps"]:
                points.append(step["polyline"]["points"])
    print("[")
    for point in points:
        print(f'"{point}",')
    print("]")
    return points


get_polyline(-6.184610, 106.889003, -6.280051, 106.826409)
