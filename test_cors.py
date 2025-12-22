import requests

response = requests.get(
    "http://localhost:8000/api/auth/me", headers={"Origin": "http://localhost:8080"}
)

print(f"Status: {response.status_code}")
print("\nCORS Headers:")
for key, value in response.headers.items():
    if "access-control" in key.lower():
        print(f"{key}: {value}")

if not any("access-control" in key.lower() for key in response.headers.keys()):
    print("NO CORS HEADERS FOUND!")
