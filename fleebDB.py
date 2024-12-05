from flask import Flask, request, jsonify
from pymongo import MongoClient
import re

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["UserInfo"]
gather = db["loginInfo"]

# Function to validate the username (same as your earlier logic)
def username_validate(username):
    pattern = r'^[A-Za-z\s]{1,20}$'
    return bool(re.match(pattern, username))

# Route for handling the signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Get the JSON data from the request
    username = data.get('username', '').strip().lower()  # Clean and lowercased username
    password = data.get('password', '').strip()

    # Validate username
    if not username_validate(username):
        return jsonify({'success': False, 'message': 'Invalid username. It must be between 1 and 20 characters and contain only letters and spaces.'})

    # Check if the username already exists in the database
    existing_user = gather.find_one({"username": username})
    if existing_user:
        return jsonify({'success': False, 'message': 'This username is already taken.'})

    # If username is valid and doesn't exist, add to database
    new_user = {"username": username, "password": password}
    gather.insert_one(new_user)

    return jsonify({'success': True, 'message': 'Account created successfully!'})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
