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
def create_user(user: User):
    # Check if the email already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already exists.")

    # Convert the Pydantic model to a dictionary and insert it
    user_dict = user.dict()
    result = users_collection.insert_one(user_dict)

    return {"inserted_id": str(result.inserted_id), "user": user_dict}

@app.get("/list_collections") #
def list_cols():
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

@app.get("/get_users")
def get_users():
    # Fetch all users from the collection
    users = list(users_collection.find())

    # Convert ObjectId to string for JSON serialization
    for user in users:
        user["_id"] = str(user["_id"])

    return {"users": users}

@app.get("/delete_col")
def delete_col():
    db.users.drop()
    return {"message": "collection dropped"}


@app.get("/get_cheets")
def get_cheets():
    # Fetch all users from the collection
    cheets = list(cheets_collection.find())

    # Convert ObjectId to string for JSON serialization
    for cheet in cheets:
        cheet["_id"] = str(cheet["_id"])

    return {"cheet": cheet.cheet}
