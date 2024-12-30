from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
import requests
from pymongo import MongoClient
from cheet import Cheet, create_cheet, get_cheets
from user import User, create_user, get_users
from llama import Query

app = FastAPI()

# Load environment variables from .env, setup the base URLs and the endpoints
load_dotenv()
LLAMA_URL = os.getenv("LLAMA_URL", "http://localhost:8000")  # Default fallback
GEN_RESPONSE_ENDPOINT = os.getenv("GEN_RESPONSE_ENDPOINT", "/gen_response")
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")  # Default fallback

# implement CORS

# MongoDB connection
client = MongoClient(MONGO_URL)
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

@app.post(GEN_RESPONSE_ENDPOINT)
def forward_request(query: Query):
    """
    Forwards the conversation history to the LLM server.
    """
    try:
        # Forward the request to the LLM server
        response = requests.post(LLAMA_URL+GEN_RESPONSE_ENDPOINT, json=query.model_dump())
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with LLM server: {e}")

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
