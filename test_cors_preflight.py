import requests

# Test OPTIONS preflight request
response = requests.options(
    "http://localhost:8000/api/auth/me",
    headers={
        "Origin": "http://localhost:8080",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "authorization,content-type",
    },
)

print(f"Preflight Status: {response.status_code}")
print("\nPreflight CORS Headers:")
for key, value in response.headers.items():
    if "access-control" in key.lower():
        print(f"{key}: {value}")
