from fastapi import FastAPI
from pymongo import MongoClient
from cheet import Cheet, create_cheet, get_cheets
from user import User, create_user, get_users

app = FastAPI()

# implement CORS

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client.chetter  # Connect to the "chetter" database
users_collection = db.users  # Load the "users" collection
cheets_collection = db.cheets # Load the "cheets" collection

@app.api_route("/create_users_col", methods=["GET", "POST"])
def create_users_collection():
    if "users" not in db.list_collection_names():
        db.users.insert_one({"placeholder": True})
    return {"message": "users collection created"}

@app.api_route("/create_cheets_col", methods = ["GET", "POST"])
def create_cheets_col():
    if "cheets" not in db.list_collection_names():
        db.cheets.insert_one({"placeholder": True})
    return {"message": "cheets collection created"}

@app.post("/create_user")
def create_user_endpoint(user: User):
    return create_user(user, users_collection)

@app.post("/create_cheet")
def create_cheet_endpoint(cheet: Cheet):
    return create_cheet(cheet, cheets_collection)

@app.get("/get_collections") # List all collections (schemas)
def list_cols():
    collections = db.list_collection_names() 
    return {"collections": collections}

@app.get("/get_users")
def get_users_endpoint():
    return get_users(users_collection)

@app.get("/get_cheets")
def get_cheats_endpoint():
    return get_cheets(cheets_collection)

@app.get("/delete_col")
def delete_col():
    db.users.drop()
    return {"message": "collection dropped"}
