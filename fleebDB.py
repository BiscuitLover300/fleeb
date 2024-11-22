from flask import Flask, request, jsonify, render_template, redirect

from pymongo import MongoClient
#for this import, copy the next line in below this into the terminal to have it set up with your mongoDB
import random
import re

#pip install pymongo

#After doing so, the code should run fine

app = Flask(__name__)


client = MongoClient("mongodb://localhost:27017/")

db = client["UserInfo"]
#collection = db["InfoList"]


#This is where we will store login info
gather = db["loginInfo"]


#This is the valdation used in signup and login
def username_validate(username):
    pattern = r'^[A-Za-z\s]{1,20}$'
    return bool(re.match(pattern, username))

#this function is how users will set up an account to check out. We could make an option of checkout to make this not mandatory to buy stuff.
 

# Route for rendering the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username_validate(username):
            return jsonify({"error": "Invalid username. Must be 1-20 letters with spaces allowed."}), 400

        if gather.find_one({"username": username}):
            return jsonify({"error": "Username already exists."}), 400

        if password != confirm_password:
            return jsonify({"error": "Passwords do not match."}), 400

        user_id = gather.estimated_document_count() + 1
        new_user = {"userID": user_id, "username": username, "password": password}
        gather.insert_one(new_user)

        return jsonify({"message": "Account created successfully!"}), 200
    return render_template('signup.html')



#this will be the login function on the website that will return the users data to them after they have set up an account

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username').lower()
    password = request.form.get('password')

    user = gather.find_one({"username": username, "password": password})
    if user:
        return jsonify({"message": f"Welcome, {username}!"}), 200
    return jsonify({"error": "Invalid username or password."}), 401

# Route to serve the login page
@app.route('/login_page', methods=['GET'])
def login_page():
    return render_template('login.html')

# Home route (redirects to login)
@app.route('/')
def home():
    return redirect('/login_page')

if __name__ == "__main__":
    app.run(debug=True)
        



            

#This part is for getting the database and collection put onto ur mongo for the first time

#sample_data = {"name": "Alice", "age": 30, "city": "New York"}
#collection.insert_one(sample_data)
#print("Data inserted successfully!")


# This will pull the information and display it in ur terminal

#document = collection.find_one({"name": "Alice"})
#print("Retrieved document:", document)