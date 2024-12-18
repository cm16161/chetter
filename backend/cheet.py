def create_cheet(cheet, cheets_collection):
    # Check if the email already exists
    #if cheets_collection.find_one({"cheet_ID": cheet.username}):
    #    raise HTTPException(status_code=400, detail="Cheet shouldn't have the same ID as another one.")

    # Convert the Pydantic model to a dictionary and insert it
    cheet_dict = cheet.dict()
    result = cheets_collection.insert_one(cheet_dict)

    cheet_dict["_id"] = str(result.inserted_id)

    return {"inserted_id": cheet_dict["_id"], "user": cheet_dict}

def get_cheets(cheets_collection):
    # Fetch all users from the collection
    cheets = list(cheets_collection.find())

    # Convert ObjectId to string for JSON serialization
    for cheet in cheets:
        cheet["_id"] = str(cheet["_id"])

    return {"cheet": cheets}