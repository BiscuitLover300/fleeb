from flask import Flask, request, jsonify
from pymongo import MongoClient
import json
import re
from flask_cors import CORS
import uuid
import os



app = Flask(__name__)
CORS(app)



sessions = {}


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

        #username validation for creating your account
        if not username or not username_validate(username):
            return jsonify({'success': False, 'message': 'Username must be between 3 and 20 characters long and contain only letters and numbers.'}), 400
        
        #strengthen this in the future for more security
        if not password or len(password) < 6:
            return jsonify({'success': False, 'message': 'Password must be at least 6 characters long.'}), 400
        #after the password has been made, we will hash it through a system that will only be kept in this code.

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
        if user['password'] != password:  
            return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401
        
        # Generate a session token
        session_token = str(uuid.uuid4())
        sessions[session_token] = username  # Save the session token

        return jsonify({'success': True, 'message': 'Login successful!', 'token': session_token}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred.', 'error': str(e)}), 500
    

@app.route('/user', methods=['GET'])
def get_user():
    try:
        token = request.headers.get('Authorization')
        if not token or token not in sessions:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401

        username = sessions[token]
        return jsonify({'success': True, 'username': username}), 200

    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred.', 'error': str(e)}), 500
    

@app.route('/products', methods=['GET'])
def get_products():
    try:
        # Load product data from the JSON file
        json_file_path = os.path.join(os.path.dirname(__file__), 'products.json')
        with open(json_file_path, 'r') as file:
            products = json.load(file)
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred while fetching products.', 'error': str(e)}), 500




#this is for adding items to the cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.json
        username = data.get('username')
        item = data.get('item')

        if not username or not item:
            return jsonify({'success': False, 'message': 'Username or item is missing.'}), 400

        # Update the user's cart in the database
        result = db['loginInfo'].update_one(
            {'username': username},
            {'$push': {'cart': item}}
        )
        if result.matched_count == 0:
            return jsonify({'success': False, 'message': 'User not found.'}), 404

        return jsonify({'success': True, 'message': 'Item added to cart.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred.', 'error': str(e)}), 500



#this one is for fetching the prexisting cart
@app.route('/cart/<username>', methods=['GET'])
def get_cart(username):
    try:
        user = db['loginInfo'].find_one({'username': username}, {'_id': 0, 'cart': 1})
        if not user:
            return jsonify({'success': False, 'message': 'User not found.'}), 404

        return jsonify({'success': True, 'cart': user.get('cart', [])}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred.', 'error': str(e)}), 500



#next we will put in the cart and card information storing system
#the card information will be ran through a complex hash to cramble the data for integrity 





if __name__ == '__main__':
    app.run(debug=True)
