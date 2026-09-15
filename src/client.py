import requests
import time
from http import HTTPStatus
from utils.APIStatus import APIStatus

print("Executing GET countries endpoint...\n")
api_url: str = "http://127.0.0.1:5000/countries"
response: requests.Response = requests.get(api_url)
status_code: int = response.status_code

print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
print("Response Text:", response.json())

print("Executing POST countries endpoint")
api_url: str = "http://127.0.0.1:5000/countries"
payload: dict = {"name": "TestCountry", "capital": "Abcdef", "area": 12345}

response: requests.Response = requests.post(api_url, json=payload)
status_code: int = response.status_code

print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
print("Response Text:", response.text)

print("Executing GET countries endpoint...\n")
api_url: str = "http://127.0.0.1:5000/countries"
response: requests.Response = requests.get(api_url)
status_code: int = response.status_code

print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
print("Response Text:", response.json())

# Authorization headers
'''
token = "your_bearer_token_here"

# Set up the authorization header
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}
'''