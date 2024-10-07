import requests
from geopy.geocoders import Nominatim
import time

# OpenSky Network API credentials
USERNAME = 'your_opensky_username'
PASSWORD = 'your_opensky_password'

# Russian military aircraft registration numbers
russian_aircraft = ['RA-41255', 'RA-75516', 'RA-86496', 'RA-86561']

# OpenSky API endpoint
API_URL = 'https://opensky-network.org/api/states/all'

# Geolocator for converting coordinates to places
geolocator = Nominatim(user_agent="geoapiExercises")

def get_flight_data():
    response = requests.get(API_URL, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        return response.json()['states']
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return []

def track_russian_flights():
    flights = get_flight_data()
    tracked_flights = []

    for flight in flights:
        registration_number = flight[0]
        if registration_number in russian_aircraft:
            lat, lon = flight[6], flight[5]
            status = 'In air' if flight[8] > 0 else 'On ground'
            try:
                location = geolocator.reverse(f"{lat}, {lon}")
                place = location.address if location else "Unknown"
            except:
                place = "Unknown"
            
            tracked_flights.append({
                'aircraft': registration_number,
                'status': status,
                'position': (lat, lon),
                'place': place,
                'last_seen': time.ctime(flight[3])
            })

    return tracked_flights

def display_flight_data(flights):
    for flight in flights:
        print(f"Aircraft: {flight['aircraft']}")
        print(f"Status: {flight['status']}")
        print(f"Position: {flight['position']} ({flight['place']})")
        print(f"Last seen: {flight['last_seen']}\n")

if __name__ == "__main__":
    tracked_flights = track_russian_flights()
    if tracked_flights:
        display_flight_data(tracked_flights)
    else:
        print("No Russian aircraft tracked.")
