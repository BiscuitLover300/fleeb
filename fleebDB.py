from pymongo import MongoClient
#for this import, copy the next line in below this into the terminal to have it set up with your mongoDB

#pip install pymongo

#After doing so, the code should run fine


client = MongoClient("mongodb://localhost:27017/")

db = client["UserInfo"]
collection = db["InfoList"]

#This part is for getting the database and collection put onto ur mongo
sample_data = {"name": "Alice", "age": 30, "city": "New York"}
collection.insert_one(sample_data)
print("Data inserted successfully!")


# This will pull the information and display it in ur terminal
document = collection.find_one({"name": "Alice"})
print("Retrieved document:", document)