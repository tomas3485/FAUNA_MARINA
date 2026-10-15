import requests

r = requests.get(
    "https://api.obis.org/v3/occurrence",
    params={"scientificname": "Delphinus delphis", "size": 3},
    timeout=30,
)
print(r.status_code)
print(r.json()["results"][0])

