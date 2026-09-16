import requests
import time
from http import HTTPStatus
from utils.APIStatus import APIStatus

print("----- Executing GET countries endpoint -----")
api_url: str = "http://127.0.0.1:5000/countries"
response: requests.Response = requests.get(api_url)
status_code: int = response.status_code

print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
if(response): print("Response Text:", response.json())

print("\n----- Executing POST countries endpoint -----")
api_url: str = "http://127.0.0.1:5000/countries"
payload: dict = {"name": "TestCountry", "capital": "Abcdef", "area": 12345}

response: requests.Response = requests.post(api_url, json=payload)
status_code: int = response.status_code

print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
if(response): print("Response Text:", response.json())

print("\n----- Executing GET countries endpoint -----")
api_url: str = "http://127.0.0.1:5000/countries"
response: requests.Response = requests.get(api_url)
status_code: int = response.status_code

print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
if(response): print("Response Text:", response.json())

# Attempting Authorization
print("\n----- Executing GET Authenticated countries endpoint -----")

headers = {"Authorization": "Bearer secret-token-123"}
api_url: str = "http://127.0.0.1:5000/countries"
response: requests.Response = requests.get(api_url, headers=headers)
status_code: int = response.status_code

print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
if(response): print("Response Text:", response.json())
