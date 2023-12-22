import requests
from core.keys.secrets import GOOGLE_MAPS_API_KEY
from pydantic import BaseModel


def request_direction(
    lat1: float, lng1: float, lat2: float, lng2: float, avoid_tolls: bool
):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json",
        params={
            "origin": f"{lat1},{lng1}",
            "destination": f"{lat2},{lng2}",
            "mode": "driving",
            "avoidTolls": avoid_tolls,
            "extraComputations": ["TOLLS"],
            "routeModifiers": {
                "vehicleInfo":{
                    "emissionType": "GASOLINE"
                },
            },
            "key": GOOGLE_MAPS_API_KEY,
        },
    ).json()
    return response


class RouteResult(BaseModel):
    id: int  # 0 = tolls, 1 = no tolls
    name: str
    distance: float  # km
    duration: int  # minutes
    polyline: list[str]
    cost: int = 0  # IDR


def get_routes(lat1: float, lng1: float, lat2: float, lng2: float) -> list[RouteResult]:
    tolls_route = request_direction(lat1, lng1, lat2, lng2, False)
    no_tolls_route = request_direction(lat1, lng1, lat2, lng2, True)
    print(tolls_route)
    return [
        RouteResult(
            id=0,
            name="Tolls",
            distance=tolls_route["routes"][0]["legs"][0]["distance"]["value"],
            duration=tolls_route["routes"][0]["legs"][0]["duration"]["value"],
            polyline=[tolls_route["routes"][0]["overview_polyline"]["points"]],
            # cost=tolls_route["routes"][0]["legs"][0]["travelAdvisory"]["tollInfo"]["estimatedPrice"][0]["nanos"],
        ),
        RouteResult(
            id=1,
            name="No Tolls",
            distance=no_tolls_route["routes"][0]["legs"][0]["distance"]["value"],
            duration=no_tolls_route["routes"][0]["legs"][0]["duration"]["value"],
            polyline=[no_tolls_route["routes"][0]["overview_polyline"]["points"]],
        ),
    ]


class SearchLocationResult(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float


def search_location(query: str) -> list[SearchLocationResult]:
    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/textsearch/json",
        params={
            "query": query,
            "key": GOOGLE_MAPS_API_KEY,
        },
    ).json()
    return [
        SearchLocationResult(
            name=result["name"],
            address=result["formatted_address"],
            latitude=result["geometry"]["location"]["lat"],
            longitude=result["geometry"]["location"]["lng"],
        )
        for result in response["results"]
    ]


if __name__ == "__main__":
    print(get_routes(-6.184610, 106.889003, -6.280051, 106.826409))
    print(search_location("fasilkom"))
