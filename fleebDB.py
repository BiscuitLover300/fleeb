from pymongo import MongoClient
#for this import, copy the next line in below this into the terminal to have it set up with your mongoDB
import random
import re

#pip install pymongo

#After doing so, the code should run fine


client = MongoClient("mongodb://localhost:27017/")

db = client["UserInfo"]
#collection = db["InfoList"]


#This is where we will store login info
gather = db["loginInfo"]




 
def signup():
    
    #this pattern will be used for login as well
    pattern  = r'^[A-Za-z\s]{1,20}$'

    def username_validate(us):
        return bool(re.match(pattern, us))


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


def log_in():
     
    pattern  = r'^[A-Za-z\s]{1,20}$'

    def username_validate(us):
        return bool(re.match(pattern, us))

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


            

#This part is for getting the database and collection put onto ur mongo
#sample_data = {"name": "Alice", "age": 30, "city": "New York"}
#collection.insert_one(sample_data)
#print("Data inserted successfully!")


# This will pull the information and display it in ur terminal
#document = collection.find_one({"name": "Alice"})
#print("Retrieved document:", document)