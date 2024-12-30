from pydantic import BaseModel, Field

# Define the input format for the API
class Query(BaseModel):
    conversation_history: list