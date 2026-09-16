echo "Executing clean run"

if [ -f "./data/user_data.json" ]; then
    rm ./data/user_data.json
fi

if [ -f "./data/users_file.json" ]; then
    rm ./data/users_file.json
fi

export FLASK_APP=src/server.py
export FLASK_ENV=development
flask run