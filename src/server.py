# server.py
from flask import Flask, request, jsonify

app: Flask = Flask(__name__)

countries: dict = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

def _find_next_id():
    return max(country["id"] for country in countries) + 1

@app.get("/countries")
def get_countries():
    return jsonify(countries)

@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

# Look into Flask-HTTPAuth
'''
# Specifying 'Bearer' as the header scheme (it defaults to 'Bearer')
auth = HTTPTokenAuth(scheme='Bearer')

# Mock database/store of tokens mapped to users
tokens = {
    "secret-token-123": "john_doe",
    "super-secret-456": "jane_smith"
}
@auth.verify_token
def verify_token(token):
    # This callback automatically receives the extracted token from the header
    if token in tokens:
        return tokens[token] # Returns the user identity if valid
    return None

@app.route('/api/protected', methods=['GET'])
@auth.login_required
def protected_route():
    current_user = auth.current_user()
    return jsonify({"message": f"Hello {current_user}, access granted!"})
'''