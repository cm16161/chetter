from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from http import HTTPMethod, HTTPStatus

app = FastAPI()

# implement CORS

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client.chetter  # Connect to the "chetter" database
users_collection = db.users  # Use the "users" collection

# Custom Pydantic model for user information
class User(BaseModel):
    username: str
    email: EmailStr  # Automatically validates email format
    password: str
    full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Auto-set timestamp
    #profile_picture: str = Field(
    #    None, regex="^(http|https)://.*$"
    #)  # Optional, must be a valid URL

class Tweet(BaseModel):
    # Omar's code
    username: str
    tweet: str

@app.post("/create_user")
def create_user(user: User):
    # Check if the email already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists.")

    # Convert the Pydantic model to a dictionary and insert it
    user_dict = user.dict()
    result = users_collection.insert_one(user_dict)

    return {"inserted_id": str(result.inserted_id), "user": user_dict}

# @app.post("/list_users")
# def list_users(user: User):
    # if users_collection.find_one("email": user.email)


@app.get("/mongodb") #
def list_schemas():
    collections = db.list_collection_names()  # List all collections (schemas)
    return {"collections": collections}   

