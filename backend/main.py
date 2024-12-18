from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI() #

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client.chetter  # Connect to the "chetter" database

@app.get("/users") #
def get_users():
    return {"message": "your mom"}

@app.get("/mongodb") #
def list_schemas():
    collections = db.list_collection_names()  # List all collections (schemas)
    return {"collections": collections}
