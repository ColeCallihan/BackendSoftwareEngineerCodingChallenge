import requests
from http import HTTPStatus
from utils.APIStatusEnum import APIStatusEnum
from utils.RESTEnum import RESTEnum
from utils.ExecuteAPICalls import execute_api_call

# Private method to make printing easier
def _response_print(response: requests.Response):
    status_code: int = response.status_code
    print(f"Status Code: {status_code}, {APIStatusEnum(status_code).name}, {HTTPStatus(status_code).description})")
    print("Response Text:", response.json())

# Define all endpoints
base_url = "http://127.0.0.1:5000/"
get_users_url: str = base_url + "get_users"
signup_url: str = base_url + "signup"
save_notes_url: str = base_url + "save_notes"
get_notes_url: str = base_url + "get_notes"
delete_notes_url: str = base_url + "delete_notes"
delete_user_url: str = base_url + "delete_user"

# Define All payloads
generic_payload: dict = {"username": "JohnSmith", "teamname": "TeamOne"}
note_one_payload: dict = {"username": "JohnSmith", "teamname": "TeamOne", "notes": "Saving this note for later..."}
note_two_payload: dict = {"username": "JohnSmith", "teamname": "TeamOne", "notes": "Did I leave my fridge open?..."}

# See if we are an active user first
print("\n----- 1) Executing GET all usernames Endpoint -----")
response: requests.Response = execute_api_call(get_users_url, RESTEnum.GET)
_response_print(response)

# Registering ourselves as an active user
print("\n----- 2) Executing POST SignUp Endpoint -----")
response = execute_api_call(signup_url, RESTEnum.POST, payload=generic_payload)

if response:
    _response_print(response)

    # extract the bearer token generated if generated
    if response.status_code == APIStatusEnum.CREATED:
        my_token: str = response.json()["token"]
        print(f"-- Generated token: {my_token} --")

        # See if we are an actual user now
        print("\n----- 3) Executing GET all usernames Endpoint -----")
        response = execute_api_call(get_users_url, RESTEnum.GET)
        _response_print(response)

        # step 4, try to save our notes with our new token
        print(f"\n----- 4) Executing POST Save Notes Endpoint using {my_token} -----")
        headers = {"Authorization": f"Bearer {my_token}"}
        response = execute_api_call(save_notes_url, RESTEnum.POST, payload=note_one_payload, headers=headers)
        _response_print(response)

        # step 5, try to save another note with new token
        print(f"\n----- 5) Executing POST Save Notes 2 Endpoint using {my_token} -----")
        response = execute_api_call(save_notes_url, RESTEnum.POST, payload=note_two_payload, headers=headers)
        _response_print(response)

        # step 6, try to read my own notes
        print("\n----- 6) Executing GET my notes Endpoint -----")
        response = execute_api_call(get_notes_url, RESTEnum.GET, payload=generic_payload, headers=headers)
        _response_print(response)

        # Step 7 try and delete my own notes
        print("\n----- 7) Executing DELETE my notes Endpoint -----")
        response = execute_api_call(delete_notes_url, RESTEnum.DELETE, payload=generic_payload, headers=headers)
        _response_print(response)

        # Check my notes have been deleted
        print("\n----- 8) Executing GET my notes Endpoint -----")
        response = execute_api_call(get_notes_url, RESTEnum.GET, payload=generic_payload, headers=headers)
        _response_print(response)

        # Delete myself as a user
        print("\n----- 9) Executing DELETE my user Endpoint -----")
        response = execute_api_call(delete_user_url, RESTEnum.DELETE, payload=generic_payload, headers=headers)
        _response_print(response)

        # See if we are actually deleted
        print("\n----- 10) Executing GET all usernames Endpoint -----")
        response = execute_api_call(get_users_url, RESTEnum.GET, payload=generic_payload, headers=headers)
        _response_print(response)

else:
    print("Response not valid")
