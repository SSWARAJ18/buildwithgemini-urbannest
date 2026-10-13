"""Geocoding and location lookup tools for UrbanNest using OpenStreetMap Nominatim."""

import json
import os
import urllib.parse
import urllib.request


def lookup_neighborhood_location(location_query: str) -> str:
    """Look up geographic coordinates, postal code, and verified neighborhood details for an address or area.

    Uses the OpenStreetMap Nominatim API from the public-apis directory to resolve real-world location data.

    Args:
        location_query: The address, neighborhood, or area to look up (e.g. 'Mission District, San Francisco' or 'Hayes Valley').

    Returns:
        JSON string containing verified address, coordinates, postal code, and OpenStreetMap link.
    """
    if not location_query:
        return json.dumps({"error": "location_query cannot be empty."})

    user_agent = os.environ.get("NOMINATIM_USER_AGENT", "UrbanNestAgent/1.0 (contact@urbannest.internal)")
    api_key = os.environ.get("GEOCODING_API_KEY", "")

    encoded_query = urllib.parse.quote(location_query)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded_query}&format=json&limit=1&addressdetails=1"
    if api_key:
        url += f"&key={api_key}"

    headers = {"User-Agent": user_agent}

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as response:
            if response.status != 200:
                return json.dumps({"error": f"API request failed with status code {response.status}"})
            data = json.loads(response.read().decode())

        if not data:
            return json.dumps({
                "found": False,
                "message": f"No location found for '{location_query}'."
            })

        first = data[0]
        lat = float(first.get("lat", 0.0))
        lon = float(first.get("lon", 0.0))
        address = first.get("address", {})

        result = {
            "found": True,
            "query": location_query,
            "display_name": first.get("display_name"),
            "latitude": lat,
            "longitude": lon,
            "neighborhood": address.get("neighbourhood") or address.get("suburb") or address.get("quarter"),
            "city": address.get("city") or address.get("town"),
            "postcode": address.get("postcode"),
            "map_url": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon}",
        }
        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": f"Failed to query location service: {str(e)}"})
