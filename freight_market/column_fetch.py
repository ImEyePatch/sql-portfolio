import requests
import json

# Replace this with the actual endpoint you're using
API_KEY = "eyJvcmciOiI2MmY2YTYxZDgyODM5ZjAwMDE4NmExY2EiLCJpZCI6IjRhYWZkNTY3NTA5YjRlOGU5OWJjZDVmMmQ0MGYyOTJiIiwiaCI6Im11cm11cjEyOCJ9"
BASE_URL = "https://api.mcleodsoftware.com/mpact-sandbox/rates"  # example placeholder
headers = {
    "Authorization": API_KEY,  # insert real token
    "Accept": "application/json"
}

# Make the request
response = requests.get(BASE_URL, headers=headers)

# Parse JSON
try:
    data = response.json()

    # If it's a list of records, inspect the first one
    if isinstance(data, list) and len(data) > 0:
        first_record = data[0]
        print("Top-level fields:")
        for key in first_record.keys():
            print("-", key)

    # If it's a dictionary with nested data (e.g. under 'results')
    elif isinstance(data, dict):
        if 'results' in data and isinstance(data['results'], list):
            print("Top-level fields inside 'results':")
            for key in data['results'][0].keys():
                print("-", key)
        else:
            print("Top-level fields:")
            for key in data.keys():
                print("-", key)

    else:
        print("Unexpected data structure:", type(data))

except json.JSONDecodeError:
    print("Failed to parse JSON. Check the API response format or credentials.")
