
# Initialize Nominatim API
geolocator = Nominatim(user_agent="my_app")

# Address you want to geocode
address = "1600 Amphitheatre Parkway, Mountain View, CA"

# Perform geocoding
location = geolocator.geocode(address)

# Print latitude and longitude
if location:
    print(f"Latitude: {location.latitude}, Longitude: {location.longitude}")
else:
    print("Location not found.")
