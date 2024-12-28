from fastapi import HTTPException
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

# Custom Pydantic model for user information
class User(BaseModel):
    username: str
    email: EmailStr  # Automatically validates email format
    password: str
    full_name: str
    created_at: datetime = Field(default_factory=datetime.now)  # Auto-set timestamp
    #profile_picture: str = Field(
    #    None, regex="^(http|https)://.*$"
    #)  # Optional, must be a valid URL

def create_user(user, users_collection):
    # Check if the email already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists.")

    # Convert the Pydantic model to a dictionary
    user_dict = user.dict()

    # Insert the user into the MongoDB collection
    result = users_collection.insert_one(user_dict)

    # Add the MongoDB '_id' as a string to the user dictionary
    user_dict["_id"] = str(result.inserted_id)

    return {"inserted_id": user_dict["_id"], "user": user_dict}

def get_users(users_collection):
    # Fetch all users from the collection
    users = list(users_collection.find())

    # Convert ObjectId to string for JSON serialization
    for user in users:
        user["_id"] = str(user["_id"])

    return {"users": users}