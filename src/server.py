# server.py
from flask import Flask, request, jsonify
from flask_httpauth import HTTPTokenAuth
from pathlib import Path

app: Flask = Flask(__name__)

# Would Make environment Variable
data_path: Path = Path("data/")

# Determine if user data already exists, if not, create it
users_file: Path = data_path / "user_data.txt"

try:
    #using "with open" ensures file safety
    with open(users_file, "x") as file:
        pass
except FileExistsError:
    print("User File already exists")

# countries: dict = [
#     {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
#     {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
#     {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
# ]

auth = HTTPTokenAuth(scheme='Bearer')

user_tokens = {
    "secret-token-123": "john_doe",
    "super-secret-456": "jane_smith"
}

@auth.verify_token
def verify_token(token):
    # This callback function lets Flask automatically receives the extracted token from the header
    if token in user_tokens:
        return user_tokens[token] # Returns the user identity if valid
    return None

# Private methods
# def _find_next_id() -> int:
#     return max(country["id"] for country in countries) + 1

# API Endpoints
# @app.get("/countries")
# def get_countries():
#     return jsonify(countries)

# @app.post("/countries")
# @auth.login_required
# def add_country():
#     if request.is_json:
#         country = request.get_json()
#         country["id"] = _find_next_id()
#         countries.append(country)
#         return country, 201
#     return {"error": "Request must be JSON"}, 415

#-SignUp
@app.post("/signup")
def sign_up():
    if request.is_json:
        user_profile = request.get_json()
        username = user_profile["username"]
        teamname = user_profile["teamname"]
#-GetUsers
#-SaveMyNotes (destructive save, will create if empty) (Create | Update)
#-GetMyNotes (Read)
#-DeleteMyNotes (Delete)