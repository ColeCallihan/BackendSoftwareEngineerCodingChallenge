import requests
import time
import json
from http import HTTPStatus
from utils.APIStatus import APIStatus

# See if we are an active user first
print("\n----- Executing GET all usernames Endpoint -----")
api_url: str = "http://127.0.0.1:5000/get_users"
response: requests.Response = requests.get(api_url)
status_code: int = response.status_code
print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
print("Response Text:", response.json())

# Registering ourselves as an active user
print("\n----- Executing POST SignUp Endpoint -----")
api_url: str = "http://127.0.0.1:5000/signup"
payload: dict = {"username": "JohnSmith", "teamname": "TeamOne"}

response: requests.Response = requests.post(api_url, json=payload)
if response:
    status_code: int = response.status_code
    print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
    print("Response Text:", response.json())

    # extract the bearer token generated if generated
    if status_code == APIStatus.CREATED:
        my_token: str = response.json()["token"]
        print("Generated token:", my_token)

        # See if we are an actual user now
        print("\n----- Executing GET all usernames Endpoint -----")
        api_url: str = "http://127.0.0.1:5000/get_users"
        response: requests.Response = requests.get(api_url)
        status_code: int = response.status_code
        print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
        print("Response Text:", response.json())

        # step 2, try to save our notes with our new token
        print("\n----- Executing POST Save Notes Endpoint -----")
        headers = {"Authorization": my_token}
        payload: dict = {"username": "JohnSmith", "teamname": "TeamOne", "notes": "Saving this note for later..."}
        api_url: str = "http://127.0.0.1:5000/save_notes"
        response: requests.Response = requests.post(api_url, headers=headers, json=payload)
        print(f"Status Code: {status_code}, {APIStatus(status_code).name}, {HTTPStatus(status_code).description})")
        print("Response Text:", response.json())
else:
    print("Response not valid")
