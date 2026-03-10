import requests

base_url = "http://localhost:8000"

# Using actual slugs from the DB
project_slugs = ["adaptive-xr-learning", "african-dataset-repository", "african-language-llm"]

for slug in project_slugs:
    url = f"{base_url}/projects/{slug}"
    response = requests.get(url)
    print(f"Project {slug}: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {url} returned {response.status_code}")
        exit(1)

print("All selected projects verified.")
