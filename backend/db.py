from motor.motor_asyncio import AsyncIOMotorClient
import os

# Load MongoDB URI from environment variable
MONGO_URL = os.getenv("MONGO_URI")  # e.g., "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"

# Create an async MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
print(client)

# Reference the database
db = client["slides"]
print(db)

# Reference a specific collection
users_collection = db["users"]
print(users_collection)
