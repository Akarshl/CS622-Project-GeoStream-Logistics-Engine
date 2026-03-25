import json
import random

def generate_logistics_data(num_drivers=200):
    random.seed(42)

    hotspots = [
        (50, 50, 8),   # City Center
        (25, 75, 6),   # Northwest Hub
        (75, 25, 6),   # Southeast Hub
        (20, 30, 5),   # Southwest Depot
        (80, 70, 5),   # Northeast Depot
        (50, 85, 4),   # North Terminal
        (50, 15, 4),   # South Terminal
        (10, 50, 3),   # West Outpost
        (90, 50, 3),   # East Outpost
    ]

    drivers = []
    drivers_per_hotspot = num_drivers // len(hotspots)
    remainder = num_drivers % len(hotspots)

    idx = 0
    for i, (cx, cy, spread) in enumerate(hotspots):
        count = drivers_per_hotspot + (1 if i < remainder else 0)
        for _ in range(count):
            x = round(max(0, min(100, random.gauss(cx, spread))), 2)
            y = round(max(0, min(100, random.gauss(cy, spread))), 2)
            drivers.append({"id": f"Driver_{idx:03d}", "coords": [x, y]})
            idx += 1

    locations = [
        "Downtown", "Airport", "Suburbs", "Industrial Park", "West End",
        "North Street", "North Avenue", "North Boulevard",
        "South Road", "South Lane", "South Plaza",
        "East Market", "East Gate", "East Yard",
        "West Harbor", "West Bridge",
        "Central Station", "Central Park", "Central Mall",
        "Riverside", "Riverside Dock", "Riverside Walk",
        "Hilltop", "Hilltop View", "Hilltop Terrace",
        "Lakeside", "Lakeside Drive",
        "Maple Avenue", "Maple Court",
        "Oak Street", "Oak Lane", "Oak Ridge",
        "Pine Road", "Pine Valley",
        "Cedar Boulevard", "Cedar Heights",
        "Elm Drive", "Elm Square",
        "Harbor Point", "Harbor Bay",
        "Midtown", "Midtown Plaza", "Midtown Crossing",
        "University District", "Tech Park", "Commerce Row",
    ]

    data = {"drivers": drivers, "locations": locations}

    with open("data/mock_data.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"Created data/mock_data.json with {len(drivers)} drivers and {len(locations)} locations.")

if __name__ == "__main__":
    generate_logistics_data()