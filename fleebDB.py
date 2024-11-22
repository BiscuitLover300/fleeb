from flask import Flask, request, jsonify, render_template, redirect

from pymongo import MongoClient
#for this import, copy the next line in below this into the terminal to have it set up with your mongoDB
import random
import re

#pip install pymongo

#After doing so, the code should run fine

#app = Flask(__name__)


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
#@app.route('/signup', methods=['GET', 'POST'])

def signup():



    #for this input segment, we will integrate gathering user data through the website for the username and password portion
    #after we do this, we will plug this into the data base.

    username = input("enter a username: ")
    if(username_validate(username) == True):


        #this will also be used for login
        username = username.lower()


        #after the user inputs their username, we will check to see if that name is in use
        search = gather.find_one({"username": username}, {"username": 1, "_id": 0})
        name = search["username"] if search else None
        if(name !=  username):

            #if the username is available, they will be prompted to enter a password
            password = input("enter a password: ")
            confirm_password = input("re-enter your password: ")

            if(password ==  confirm_password):
                print("Your username is: ", username, "\nYour password is: ", password)

                #this will be a unique number assigned to each user.
                #userID = random.randint()
                userID = 0
                new_user = {"userID": userID,"username": username, "password": password,}
                gather.insert_one(new_user)
            else:
                print("passwords do not match")
        
            
        else:
            print("This username is already registered.")
    else:
        print("Invalid username. Username must be between 1 and 20 letters with spaces allowed.")



#this will be the login function on the website that will return the users data to them after they have set up an account

def log_in():
     

    username = input("enter your username: ")

    if(username_validate(username) == True):

        username = username.lower()


        search = gather.find_one({"username": username}, {"username": 1, "_id": 0})
        name = search["username"] if search else None
        if(name ==  username):


            password = input("enter your password: ")

            pass_search = gather.find_one({"password": password}, {"password": 1, "_id": 0})
            word =  pass_search["password"] if search else None

            if(word == password):
                print("Welcome " + username + "!")
            else:
                print("incorrect password, please try again.")
        else:
            print("No entry of this user, if you want to make an account, click sign up!")
    else:
        print("No vaild user entered, please try again.")

        


#signup()
#log_in()


            

#This part is for getting the database and collection put onto ur mongo for the first time

#sample_data = {"name": "Alice", "age": 30, "city": "New York"}
#collection.insert_one(sample_data)
#print("Data inserted successfully!")


# This will pull the information and display it in ur terminal

#document = collection.find_one({"name": "Alice"})
#print("Retrieved document:", document)