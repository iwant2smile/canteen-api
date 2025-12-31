import random
import requests

BASE = "http://127.0.0.1:8000"

def post(path, json):
    r = requests.post(BASE + path, json=json)
    r.raise_for_status()
    return r.json()

def main():
    clients = []
    for i in range(50):
        c = post("/clients/", {
            "full_name": f"Client {i}",
            "email": f"client{i}@example.com"
        })
        clients.append(c["id"])

    dishes = []
    categories = ["soup", "main", "dessert", "drink"]
    for i in range(50):
        d = post("/dishes/", {
            "name": f"Dish {i}",
            "category": random.choice(categories),
            "price": round(random.uniform(1, 20), 2),
            "description": f"Dish number {i}"
        })
        dishes.append(d["id"])

    for _ in range(200):
        post("/orders/", {
            "client_id": random.choice(clients),
            "dish_id": random.choice(dishes),
            "quantity": random.randint(1, 5)
        })

    print("Seed done")

if __name__ == "__main__":
    main()
