import googlemaps
from fastapi import FastAPI

app = FastAPI()

# Initialize Google Maps client with your API key
gmaps = googlemaps.Client(key='YOUR_API_KEY')

@app.get("/get_coordinates")
async def get_coordinates(address: str):
    # Use the Geocoding API to convert address to coordinates
    geocode_result = gmaps.geocode(address)

    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return {"latitude": location['lat'], "longitude": location['lng']}
    else:
        return {"error": "Address not found"}
