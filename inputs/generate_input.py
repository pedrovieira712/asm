import json
import uuid
import random
import string

INPUT_FILE = "../Utils/api_locations/distritos_municipios_freguesias.json"
OUTPUT_FILE = "scenario_test_all.json"

VEHICLE_TYPES = ["car", "motorcycle", "truck", "caravan", "bus"]
USER_TYPES = ["normal", "pregnant", "reduced_mobility", "elderly"]


def random_plate():
    letters = string.ascii_uppercase
    return f"{random.choice(letters)}{random.choice(letters)}-" \
           f"{random.randint(10,99)}-" \
           f"{random.choice(letters)}{random.choice(letters)}"


def random_subset(values):
    size = random.randint(1, len(values))
    return random.sample(values, size)


def random_max_height():
    return round(random.choice([1.5, 2.0, 2.5, 3.0]), 1)


def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_parks(data):
    parks = []
    park_counter = 1

    for distrito_nome, distrito in data.items():
        coords = distrito.get("coordenadas")
        if not coords:
            continue 

        lat = coords[1]  
        lon = coords[0]

        park = {
            "id": f"P{park_counter}",
            "location": [lat, lon],
            "name": f"Parque {distrito_nome}",
            "capacity": 10,
            "max_height": random_max_height(),
            "tarifa_minuto": round(random.uniform(0.03, 0.08), 2),
            "hora_fecho": "23:00",
            "multa_fixa": 20.0,
            "spots": [
                {
                    "spot_id": f"L{i}",
                    "allowed_vehicle_types": random_subset(VEHICLE_TYPES),
                    "allowed_user_types": random_subset(USER_TYPES)
                }
                for i in range(1, 11)
            ]
        }

        parks.append(park)
        park_counter += 1

    return parks


def generate_vehicles(parks):
    vehicles = []
    num_vehicles = len(parks) * 2

    for _ in range(num_vehicles):
        park = random.choice(parks)

        vehicle = {
            "plate": random_plate(),
            "vehicle_type": random.choice(VEHICLE_TYPES),
            "user_type": random.choice(USER_TYPES),
            "location": park["location"],
            "vehicle_height": round(random.uniform(1.4, 2.0), 2),
            "redirect": random.choice([True, False]),
            "skip_payment": random.choice([True, False])
        }

        vehicles.append(vehicle)

    return vehicles


def main():
    data = load_data()

    parks = generate_parks(data)
    vehicles = generate_vehicles(parks)

    output = {
        "parks": parks,
        "vehicles": vehicles
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    print("JSON de teste gerado com sucesso")
    print(f"Parques: {len(parks)}")
    print(f"Veículos: {len(vehicles)}")


if __name__ == "__main__":
    main()