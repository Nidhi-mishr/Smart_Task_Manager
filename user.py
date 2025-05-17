import json
from werkzeug.security import generate_password_hash, check_password_hash
import os

# File path to store user data
USER_FILE = 'users.json'

# Load users from the JSON file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save users to the JSON file
def save_users(users):
    with open(USER_FILE, 'w') as file:
        json.dump(users, file)

users = load_users()  # Load users at the start

def add_user(username, password):
    if username not in users:
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        save_users(users)  # Save the updated users to the file
        return True
    return False

def check_user(username, password):
    stored_hash = users.get(username)
    if stored_hash:
        return check_password_hash(stored_hash, password)
    return False
