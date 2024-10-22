import requests
import json

# Define the API URL


start_date = '2023-10-16'  # Replace with your desired start date
end_date = '2023-10-16'

url = f'https://app.calltools.io/api/agentperformance/?start_date={start_date}&end_date={end_date}'

# Set the headers with the API key included
headers = {
    'accept': 'application/json',
    'Authorization': 'Token 2b0ab0c0114701629c8ad8b787780f2fa2fe9081',  # Replace YOUR_API_KEY with the actual key
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse and print the JSON response
    data = response.json()

    # Print the indented JSON response
    print(json.dumps(data, indent=4))
else:
    print(f"Error: {response.status_code}, {response.text}")
