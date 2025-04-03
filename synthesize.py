import time
import json
import random

from bson import ObjectId


with open('sales.json', 'r') as f:
    original = f.read().splitlines()


possible_items = set()
for entry in original:
    entry = json.loads(entry)
    for x in entry['items']:
        x = json.dumps(x)
        if x not in possible_items:
            possible_items.add(x)

synthesized = [
    {
        "_id": {
            "$oid": str(ObjectId())
        },
        "saleDate": {
            "$date": {
                "$numberLong": str(random.randint(int((time.time() - 2 * 365 * 24 * 60 * 60) * 1000), int(time.time() * 1000)))
            }
        },
        "items": [
            json.loads(random.choice(list(possible_items)))
            for _ in range(random.randint(4, 10))
        ],
        "storeLocation": random.choice(["Denver", "Seattle", "London", "Austin", "New York", "San Diego"]),
        "customer": {
            "gender": random.choice(["M", "F"]),
            "age": {"$numberInt": str(random.randint(18, 75))},
            "email": f"{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=6))}@{''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))}.com",
            "satisfaction": {"$numberInt": str(random.randint(1, 5))}
        },
        "couponUsed": random.choice([True, False]),
        "purchaseMethod": random.choice(["Online", "Phone", "In store"])
    }
    for _ in range(15000)
]

with open('sales_synthesized.json', 'a') as f:
    for line in synthesized:
        f.write(json.dumps(line) + '\n')

print('Written new data!')
