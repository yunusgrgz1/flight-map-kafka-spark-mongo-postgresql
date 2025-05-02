from flask import Flask, jsonify
from datetime import datetime, timedelta
import random
import math

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

# 60 cities worldwide
AIRPORTS = [
    {"city": "Berlin", "airport": "Berlin Brandenburg Airport", "lat": 52.3667, "lon": 13.5033},
    {"city": "Paris", "airport": "Charles de Gaulle Airport", "lat": 49.0097, "lon": 2.5479},
    {"city": "Amsterdam", "airport": "Schiphol Airport", "lat": 52.3105, "lon": 4.7683},
    {"city": "Istanbul", "airport": "Istanbul Airport", "lat": 41.2753, "lon": 28.7519},
    {"city": "London", "airport": "Heathrow Airport", "lat": 51.4700, "lon": -0.4543},
    {"city": "New York", "airport": "JFK International Airport", "lat": 40.6413, "lon": -73.7781},
    {"city": "Los Angeles", "airport": "LAX Airport", "lat": 33.9416, "lon": -118.4085},
    {"city": "Tokyo", "airport": "Haneda Airport", "lat": 35.5494, "lon": 139.7798},
    {"city": "Sydney", "airport": "Kingsford Smith Airport", "lat": -33.9399, "lon": 151.1753},
    {"city": "Dubai", "airport": "Dubai International Airport", "lat": 25.2532, "lon": 55.3657},
    {"city": "Beijing", "airport": "Beijing Capital Airport", "lat": 40.0801, "lon": 116.5846},
    {"city": "Toronto", "airport": "Pearson Airport", "lat": 43.6777, "lon": -79.6248},
    {"city": "Mexico City", "airport": "Benito Juarez Airport", "lat": 19.4361, "lon": -99.0719},
    {"city": "Sao Paulo", "airport": "Guarulhos Airport", "lat": -23.4356, "lon": -46.4731},
    {"city": "Cape Town", "airport": "Cape Town Airport", "lat": -33.9715, "lon": 18.6021},
    {"city": "Moscow", "airport": "Sheremetyevo Airport", "lat": 55.9726, "lon": 37.4146},
    {"city": "Madrid", "airport": "Barajas Airport", "lat": 40.4893, "lon": -3.5676},
    {"city": "Rome", "airport": "Fiumicino Airport", "lat": 41.8003, "lon": 12.2389},
    {"city": "Bangkok", "airport": "Suvarnabhumi Airport", "lat": 13.6900, "lon": 100.7501},
    {"city": "Singapore", "airport": "Changi Airport", "lat": 1.3644, "lon": 103.9915},
    {"city": "Seoul", "airport": "Incheon Airport", "lat": 37.4602, "lon": 126.4407},
    {"city": "Delhi", "airport": "Indira Gandhi Airport", "lat": 28.5562, "lon": 77.1000},
    {"city": "Cairo", "airport": "Cairo International", "lat": 30.1120, "lon": 31.4000},
    {"city": "Athens", "airport": "Eleftherios Venizelos", "lat": 37.9364, "lon": 23.9475},
    {"city": "Lisbon", "airport": "Humberto Delgado", "lat": 38.7742, "lon": -9.1342},
    {"city": "Vienna", "airport": "Vienna International", "lat": 48.1103, "lon": 16.5697},
    {"city": "Zurich", "airport": "Zurich Airport", "lat": 47.4581, "lon": 8.5555},
    {"city": "Munich", "airport": "Franz Josef Strauss", "lat": 48.3538, "lon": 11.7861},
    {"city": "Oslo", "airport": "Gardermoen Airport", "lat": 60.1939, "lon": 11.1004},
    {"city": "Stockholm", "airport": "Arlanda Airport", "lat": 59.6519, "lon": 17.9186},
    {"city": "Helsinki", "airport": "Helsinki-Vantaa", "lat": 60.3172, "lon": 24.9633},
    {"city": "Brussels", "airport": "Zaventem Airport", "lat": 50.9014, "lon": 4.4844},
    {"city": "Doha", "airport": "Hamad Intl Airport", "lat": 25.2736, "lon": 51.6080},
    {"city": "Abu Dhabi", "airport": "Abu Dhabi Intl", "lat": 24.4329, "lon": 54.6511},
    {"city": "Hong Kong", "airport": "Chek Lap Kok", "lat": 22.3080, "lon": 113.9185},
    {"city": "Manila", "airport": "Ninoy Aquino", "lat": 14.5086, "lon": 121.0198},
    {"city": "Buenos Aires", "airport": "Ezeiza Airport", "lat": -34.8222, "lon": -58.5358},
    {"city": "Jakarta", "airport": "Soekarno-Hatta", "lat": -6.1256, "lon": 106.6559},
    {"city": "Kuala Lumpur", "airport": "KLIA", "lat": 2.7456, "lon": 101.7072},
    {"city": "Auckland", "airport": "Auckland Airport", "lat": -37.0082, "lon": 174.7850},
    {"city": "Chicago", "airport": "O'Hare International Airport", "lat": 41.9742, "lon": -87.9073},
    {"city": "San Francisco", "airport": "San Francisco International Airport", "lat": 37.6213, "lon": -122.3790},
    {"city": "Atlanta", "airport": "Hartsfield-Jackson Airport", "lat": 33.6407, "lon": -84.4277},
    {"city": "Miami", "airport": "Miami International Airport", "lat": 25.7959, "lon": -80.2871},
    {"city": "Boston", "airport": "Logan International Airport", "lat": 42.3656, "lon": -71.0096},
    {"city": "Vancouver", "airport": "Vancouver International Airport", "lat": 49.1967, "lon": -123.1815},
    {"city": "Montreal", "airport": "Montréal-Trudeau Airport", "lat": 45.4706, "lon": -73.7408},
    {"city": "Lima", "airport": "Jorge Chavez Airport", "lat": -12.0219, "lon": -77.1143},
    {"city": "Bogotá", "airport": "El Dorado International", "lat": 4.7016, "lon": -74.1469},
    {"city": "Santiago", "airport": "Arturo Merino Benítez Airport", "lat": -33.3929, "lon": -70.7858},
    {"city": "Casablanca", "airport": "Mohammed V Airport", "lat": 33.3675, "lon": -7.5899},
    {"city": "Nairobi", "airport": "Jomo Kenyatta Airport", "lat": -1.3192, "lon": 36.9275},
    {"city": "Lagos", "airport": "Murtala Muhammed Airport", "lat": 6.5774, "lon": 3.3212},
    {"city": "Johannesburg", "airport": "O. R. Tambo Airport", "lat": -26.1337, "lon": 28.2420},
    {"city": "Karachi", "airport": "Jinnah International Airport", "lat": 24.9065, "lon": 67.1608},
    {"city": "Tehran", "airport": "Imam Khomeini Airport", "lat": 35.4161, "lon": 51.1522},
    {"city": "Riyadh", "airport": "King Khalid Airport", "lat": 24.9576, "lon": 46.6987},
    {"city": "Baghdad", "airport": "Baghdad International Airport", "lat": 33.2625, "lon": 44.2346},
    {"city": "Tashkent", "airport": "Islam Karimov Tashkent Intl", "lat": 41.2579, "lon": 69.2817},
    {"city": "Doha", "airport": "Hamad International Airport", "lat": 25.2736, "lon": 51.6080}

]

AIRLINES = ["Lufthansa", "Turkish Airlines", "Emirates", "Delta", "Pegasus Airlines", "Qatar Airways", "KLM", "Ryan Air", "Singapore Airlines", "Qantas", "Japan Airlines" ]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def move_towards(lat1, lon1, lat2, lon2, dist_km):
    total_dist = haversine(lat1, lon1, lat2, lon2)
    if dist_km >= total_dist:
        return lat2, lon2
    ratio = dist_km / total_dist
    lat = lat1 + (lat2 - lat1) * ratio
    lon = lon1 + (lon2 - lon1) * ratio
    return lat, lon



def calculate_bearing(lat1, lon1, lat2, lon2):
    """
    Hesaplama sonucu: 0-359 derece arasında bir yön (kuzey = 0, doğu = 90, güney = 180, batı = 270)
    """
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    diff_long = math.radians(lon2 - lon1)

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - \
        math.sin(lat1) * math.cos(lat2) * math.cos(diff_long)

    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing




# flights
flights = []
for i in range(100): #you can specify this number according to how hard you want to try :)

    # random departures and arrivals
    departure, arrival = random.sample(AIRPORTS, 2)
    lat1, lon1 = departure["lat"], departure["lon"]
    lat2, lon2 = arrival["lat"], arrival["lon"]

    direction = calculate_bearing(lat1, lon1, lat2, lon2)

    distance_km = haversine(lat1, lon1, lat2, lon2)

    speed = random.randint(800, 920)

    duration_hours = distance_km / speed

    now = datetime.utcnow()
    dep_offset = timedelta(minutes=random.randint(-60, 30))
    sched_dep = now + dep_offset
    sched_arr = sched_dep + timedelta(hours=duration_hours)
    actual_dep = sched_dep + timedelta(minutes=random.randint(0, 5))

    flights.append({
        "flight_id": i + 1,
        "airline": random.choice(AIRLINES),
        "departure_city": departure["city"],
        "departure_airport": departure["airport"],
        "arrival_city": arrival["city"],
        "arrival_airport": arrival["airport"],
        "scheduled_departure_time": sched_dep.isoformat(),
        "scheduled_arrival_time": sched_arr.isoformat(),
        "actual_departure_time": actual_dep.isoformat(),
        "start_time": actual_dep,
        "lat": lat1,
        "lon": lon1,
        "dest_lat": lat2,
        "dest_lon": lon2,
        "speed": speed,
        "direction": direction,
        "distance_travelled": 0,
        "actual_landed_time": None
    })

@app.route("/api/flights")
def get_flights():
    now = datetime.utcnow()
    updated_flights = []
    for flight in flights:
        elapsed_hours = (now - flight["start_time"]).total_seconds() / 3600
        total_dist = haversine(flight["lat"], flight["lon"], flight["dest_lat"], flight["dest_lon"])
        distance = flight["speed"] * max(0, elapsed_hours)
        progress = min(distance / total_dist, 1.0) if total_dist > 0 else 1.0

        
        if progress >= 1.0:
            flight_status = "landed"
            speed = 0
            altitude = 0
            actual_landed_time = flight.get("actual_landed_time") or now.isoformat()
            new_lat, new_lon = flight["dest_lat"], flight["dest_lon"]
        else:
            flight_status = "active"
            actual_landed_time = None

            if progress < 0.1:
                speed = flight["speed"] * (progress / 0.1)
            elif progress > 0.9:
                speed = flight["speed"] * ((1 - progress) / 0.1)
            else:
                speed = flight["speed"]

            if progress < 0.2:
                altitude = 10500 * (progress / 0.2)
            elif progress > 0.8:
                altitude = 10500 * ((1 - progress) / 0.2)
            else:
                altitude = 10500

            new_lat, new_lon = move_towards(
                flight["lat"], flight["lon"], flight["dest_lat"], flight["dest_lon"], distance
            )

        updated_flights.append({
            **flight,
            "current_location": {"latitude": round(new_lat, 4), "longitude": round(new_lon, 4)},
            "current_speed_km_h": round(speed),
            "current_altitude_m": round(altitude),
            "distance_travelled_km": round(distance, 2),
            "flight_status": flight_status,
            "actual_landed_time": actual_landed_time
        })

    return jsonify({"flights": updated_flights})

if __name__ == "__main__":
    app.run(debug=True)
    
#http://127.0.0.1:5000/api/flights
