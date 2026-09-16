# server.py
from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth
from pathlib import Path
from utils.user import User
from utils.GenerateToken import generate_token
import json

app: Flask = Flask(__name__)

# Would Make environment Variable
data_path: Path = Path("data/")

# Determine if user data already exists, if not, create it
users_file: Path = data_path / "users_file.json"

try:
    #using "with open" ensures file safety
    with open(users_file, "x") as file:
        dummy_user: User = User(id=0, username="ExampleName", teamname="ExampleTeam", token="abcdef")
        file.write(dummy_user.model_dump_json())
        print("Creating dummy user file")
except FileExistsError:
    print("User File already exists")


auth = HTTPTokenAuth(scheme='Bearer')

user_tokens = {
    "secret-token-123": "john_doe",
    "super-secret-456": "jane_smith"
}

@auth.verify_token
def verify_token(token):
    # This callback function lets Flask automatically receives the extracted token from the header
    user_list: list[User] = _get_user_list()
    all_tokens: list[str] = []
    for user in user_list:
        all_tokens.append(user.token)

    if token in all_tokens:
        return user_tokens[token] # Returns the user identity if valid
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
        print(note)
        return jsonify(note), 201
    else:
        return {"error": "Request must be JSON"}, 415

#-GetMyNotes (Read)
#-DeleteMyNotes (Delete)
#-DeleteUser