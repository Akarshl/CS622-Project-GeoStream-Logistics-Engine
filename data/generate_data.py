import json
import random

def generate_logistics_data(num_drivers=50, num_locations=20):
    data = {
        "drivers": [],
        "locations": ["Downtown", "Airport", "Suburbs", "Industrial Park", "West End"]
    }

    # Generate random drivers across a 100x100 grid
    for i in range(num_drivers):
        driver = {
            "id": f"Driver_{i:03d}",
            "coords": (round(random.uniform(0, 100), 2), round(random.uniform(0, 100), 2))
        }
        data["drivers"].append(driver)

    # Add more specific street names for the Radix Tree to index
    extra_locations = ["North Street", "North Avenue", "North Boulevard", "South Road", "South Lane"]
    data["locations"].extend(extra_locations)

    with open("data/mock_data.json", "w") as f:
        json.dump(data, f, indent=4)
    print("✅ Created data/mock_data.json with 50 drivers and 30 locations.")

if __name__ == "__main__":
    generate_logistics_data()