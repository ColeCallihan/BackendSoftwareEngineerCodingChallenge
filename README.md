## BackendSoftwareEngineerCodingChallenge

# How to Run
First create a python virtual environment  
python -m venv venv 

Install Flask, Pydantic and Flask-HTTPAuth  
python -m pip install flask  
python -m pip install pydantic  
python -m pip install flask  

To run the flask server:  
./scripts/run.sh

To run cleanly (deleting the user file and user data json files)  
./scripts/clean_run.sh

To Test the client side  
python src/client.py

# Research:
https://realpython.com/api-integration-in-python/

# Language:

Python  
Its a language I am comfortable with. (3 years of experience + teaching python in a professional college level context)  
Interpreted language - Great for fast/rapid prototyping and can run on anything while trading off slower execution speed in the long run and having to deliver uncompiled/public source code files for a prototype.  

# Framework:

Flask (Http and routing, good midpoint)  
FastAPI (Starlette and Pydantic, performant 'microframework')  
Django REST (Built on top of Django, more for fullstack)  

# Schema:

# Endpoints:
(Basic CRUD operations)  
-SignUp  
-GetUsers  
-SaveMyNotes (destructive save, will create if empty) (Create | Update)  
-GetMyNotes (Read)  
-DeleteMyNotes (Delete)  

# Storage:

Local storage on the server  
local variables (Map, hashset, list/array), local files (JSON txt files, csv text files)  
SQL Database  
NoSQL Database  

# What's in Scope: 

Ability to send notes over the API endpoint  
Endpoint can make distinctions between Users + Teams  

# Assumptions:
"Shared amongst several small teams"
Identifying between the teams + team members + security is important  
"Capture and work with their notes"  
Need to be able to send notes as well as retrieve them  
Store data as JSON locally, with the UID as the filename  

Protect data in transit, use bearer tokens for now  

# Design Decisions:

Save vs Update, decided to keep as just a destructive save for now, but would want something else to prevent users from accidentally deleting notes  
Not storing much in stack memory, trying to keep it atomic in case API server randomly fails  
Check for users in the users file upon signup using the username and teamname combined as the UUID. Keeps the signup idempotent (although this does increase the likelihood of collisions of ID's)  

# What I would change, add, or stop doing if I had more time:

Add: JSON Web Tokens to protect data in transit further  
Multiple notes per user, saved as something other than just a raw string  
Add: logic to determine if constructive vs destructive save is needed  
Add: Encryption for saving the user_data file when at rest  
Save users as something better than a pipe-separated file (definitely a proper database)  
The database would also allow for easier updates to each person's notes (also not having to keep it just a string, but could support rich markuptext) (Or leverage the PUT endpoint)  
Add: More input sanitization. I don't want users running things through the API endpoint as that poses an injection attack security risk  
Add: more fidelity when deleting notes instead of deleting everything.  
Change: User ID is a bit useless now, meant it to be the UUID, but would use a library like pythons UUID  