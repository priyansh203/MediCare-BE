"""MongoDB database connection and configuration."""

import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Create MongoDB client
client = AsyncIOMotorClient(
    settings.MONGO_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

# Get database
db = client[settings.MONGO_DB_NAME]

# Collections
users_collection = db["users"]
sessions_collection = db["sessions"]
threads_collection = db["threads"]
patients_collection = db["patients"]

async def connect_to_mongo():
    """Connect to MongoDB and verify connection."""
    try:
        await client.admin.command('ping')
        print(f"Connected to MongoDB: {settings.MONGO_DB_NAME}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection."""
    client.close()
    print("Closed MongoDB connection")