from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
import re
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


# MongoDB Connections
client = MongoClient("mongodb://localhost:27017/")
db = client['UserInfo']  # Database
collection = db['loginInfo']  # Collection

#username setup requirements
def username_validate(username):
    pattern = r'^[A-Za-z0-9]{3,20}$'
    return bool(re.match(pattern, username))


#route for the signup process on signup.html
@app.route('/signup', methods=['POST'])
def signup():
    try:
        # Parse JSON data
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        
        if not username or not username_validate(username):
            return jsonify({'success': False, 'message': 'Username must be between 3 and 20 characters long and contain only letters and numbers.'}), 400
        
        #strengthen this
        if not password or len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters long.'}), 400

        # Check if username already exists
        if collection.find_one({'username': username}):
            return jsonify({'success': False, 'message': 'Username already exists.'}), 409

        # Save to database
        user_data = {
            "username": username,
            "password": password  # For production, hash passwords before saving
        }
        collection.insert_one(user_data)

        return jsonify({'success': True, 'message': 'User registered successfully!'}), 201

    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred.', 'error': str(e)}), 500
    
#route for the login process on login.html
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required.'}), 400

        # Find the user in the database
        user = collection.find_one({'username': username})
        if not user:
            return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

        # Validate password
        if user['password'] != password:  #we need to add input validation to this
            return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

        return jsonify({'success': True, 'message': 'Login successful!'}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred.', 'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
