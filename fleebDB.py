from pymongo import MongoClient
#for this import, copy the next line in below this into the terminal to have it set up with your mongoDB
import random


#pip install pymongo

#After doing so, the code should run fine


client = MongoClient("mongodb://localhost:27017/")

db = client["UserInfo"]
#collection = db["InfoList"]


#This is where we will store login info
gather = db["loginInfo"]




 
def signup():

    #for this input segment, we will integrate gathering user data through the website for the username and password portion
    #after we do this, we will plug this into the data base.

    username = input("enter a username: ")
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


def log_in():
        username = input("enter your username: ")
        password = input("enter your password: ")
        
        if(gather.find_one(username) and gather.find_one(password)):
            return "welcome, " + username
            
        else:
            return "Incorrect Login. For new users, please click Sign Up."
            
        






signup()
#log_in()


            

#This part is for getting the database and collection put onto ur mongo
#sample_data = {"name": "Alice", "age": 30, "city": "New York"}
#collection.insert_one(sample_data)
#print("Data inserted successfully!")


# This will pull the information and display it in ur terminal
#document = collection.find_one({"name": "Alice"})
#print("Retrieved document:", document)