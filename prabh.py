import requests

# Define the URL and headers
url = "https://www.wixapis.com/oauth2/token"
headers = {"Content-Type": "application/json"}

# Define the data payload
data = {
    "clientId": "0950ff77-70a9-4978-b9ea-32c06a5e855e",  # Replace <CLIENT_ID> with your actual client ID
    "grantType": "anonymous",
}

# Make the POST request
response = requests.post(url, headers=headers, json=data)

# Check the response
if response.status_code == 200:
    # Successful request
    print("Access Token:", response.json())
else:
    # Handle error
    print("Error:", response.status_code, response.text)
