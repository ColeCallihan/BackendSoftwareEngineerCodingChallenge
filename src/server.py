# server.py
from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth
from pathlib import Path
from utils.user import User
from utils.GenerateToken import generate_token
import json

app: Flask = Flask(__name__)

# Would Make environment Variable
local_storage: Path = Path("data/")

# Determine if user data already exists, if not, create it
users_file: Path = local_storage / "users_file.json"
data_file: Path = local_storage / "user_data.json"

try:
    #using "with open" ensures file safety
    with open(users_file, "x") as file:
        dummy_user: User = User(id=0, username="ExampleName", teamname="ExampleTeam", token="abcdef")
        file.write(dummy_user.model_dump_json())
        print("Creating dummy user file")
except FileExistsError:
    print("User File already exists")

try:
    #using "with open" ensures file safety
    with open(data_file, "x") as file:
        dummy_dict: dict = {"ExampleNameExampleTeam": ["A possible Note"]}
        json.dump(dummy_dict, file, indent=4)
        print("Creating dummy data file")
except FileExistsError:
    print("Data File already exists")

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    # This callback function lets Flask automatically receives the extracted token from the header
    user_list: list[User] = _get_user_list()
    all_tokens: list[str] = []
    for user in user_list:
        all_tokens.append(user.token)

    if token in all_tokens:
        return token # Returns the token if valid
    return None

# Private methods
def _get_user_list() -> list[User]:
    user_list: list = []
    with open(users_file, "r") as file:
        raw_list: list = file.read().split("|")

        for user_str in raw_list:
            user = User.model_validate_json(user_str)
            user_list.append(user)
    return user_list

def _gather_valid_users():
    user_list: list[User] = _get_user_list()

    all_usernames: list[str] = []
    for user in user_list:
        all_usernames.append(user.username)
    return all_usernames

def _save_a_user(username: str, teamname: str) -> User:
    # Returns true if able to add, false if duplicated
    user_list: list[User] = _get_user_list()

    # check if user is unique (also find max id)
    new_user: User = User(id=0, username=username, teamname=teamname, token=generate_token(6))

    max_id: int = 0
    for old_user in user_list:
        max_id = old_user.id
        if new_user == old_user:
            return

    # add user to file
    new_user.id = max_id + 1
    with open(users_file, "a") as file:
        file.write(f"|{new_user.model_dump_json()}")
    return new_user

def _save_note(note: str, user_team:str) -> bool:
    # first, read in user data
    user_data_dict: dict

    with open(data_file, "r") as file:
        user_data_dict = json.load(file)

    if user_team in user_data_dict:
        user_data_dict[user_team].append(note)
    else:
        # if user already exists, create list
        user_data_dict[user_team] = [note]

    # save dict back to file
    with open(data_file, "w") as file:
        json.dump(user_data_dict, file, indent=4)
    return True

def _get_notes(user_team: str) -> list[str] | None:
    # first, read in user data
    user_data_dict: dict

    with open(data_file, "r") as file:
        user_data_dict = json.load(file)

    # See if user exists
    if user_team in user_data_dict:
        return user_data_dict[user_team]
    # if not, return nothing

#-SignUp
@app.post("/signup")
def sign_up():
    if request.is_json:
        user_profile = request.get_json()
        username = user_profile["username"]
        teamname = user_profile["teamname"]
        new_user: User = _save_a_user(username, teamname)
        if new_user:
            return new_user.model_dump_json(), 201
        else:
            return {"Message": "User already exists"}, 200
    return {"error": "Request must be JSON"}, 415

#-GetUsers
@app.get("/get_users")
def get_users():
    return jsonify(_gather_valid_users())

# Authorized Calls
#-SaveMyNotes (destructive save, will create if empty) (Create | Update)
@app.post("/save_notes")
@auth.login_required
def save_notes():
    if request.is_json:
        payload = request.get_json()
        username = payload["username"]
        teamname = payload["teamname"]
        note: str = payload["notes"]
        if _save_note(note, username + teamname):
            return jsonify(note), 201
        else:
            return {"Message": "Unable to save note"}, 200
    else:
        return {"error": "Request must be JSON"}, 415

#-GetMyNotes (Read)
@app.get("/get_notes")
@auth.login_required
def read_notes():
    if request.is_json:
        payload = request.get_json()
        username = payload["username"]
        teamname = payload["teamname"]
        notes: list[str] = _get_notes(username+teamname)
        if notes:
            return notes
        else:
            return {"Message": "No notes saved"}
    else:
        return {"error": "Request must be JSON"}, 415

#-DeleteMyNotes (Delete)
#-DeleteUser