from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
from http import HTTPMethod, HTTPStatus
from bson import ObjectId

app = FastAPI()

# implement CORS

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client.chetter  # Connect to the "chetter" database
users_collection = db.users  # Use the "users" collection
cheets_collection = db.cheets # Use the "cheets" collection

# Custom Pydantic model for user information
class User(BaseModel):
    username: str
    email: str  # Automatically validates email format
    password: str
    full_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Auto-set timestamp
    #profile_picture: str = Field(
    #    None, regex="^(http|https)://.*$"
    #)  # Optional, must be a valid URL

class PydanticObjectId(ObjectId): #  We need to overwrite ObjectID here to get it working with Pydantic
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)
    
class Cheet(BaseModel):
    # Omar's code
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id") # Auto-set new cheet ID
    username: str
    cheet: str
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Auto-set timestamp

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

@app.post("/create_cheet")
def create_cheet(cheet: Cheet):
    # Check if the email already exists
    if cheets_collection.find_one({"cheet_ID": cheet.cheet_ID}):
        raise HTTPException(status_code=400, detail="Cheet shouldn't have the same ID as another one.")

    # Convert the Pydantic model to a dictionary and insert it
    cheet_dict = cheet.dict()
    result = cheets_collection.insert_one(cheet_dict)

    return {"inserted_id": str(result.inserted_id), "cheet": cheet_dict}