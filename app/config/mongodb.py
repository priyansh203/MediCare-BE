"""MongoDB database connection and configuration."""

import certifi
from motor.motor_asyncio import AsyncIOMotorClient
import os
from urllib.parse import quote_plus, urlparse, urlunparse
from dotenv import load_dotenv

load_dotenv()

def encode_mongodb_uri(uri: str) -> str:
    """Encode MongoDB URI username and password according to RFC 3986."""
    if not uri:
        return uri
    
    parsed = urlparse(uri)
    if parsed.username or parsed.password:
        username = quote_plus(parsed.username) if parsed.username else None
        password = quote_plus(parsed.password) if parsed.password else None
        
        netloc = f"{username}:{password}@{parsed.hostname}" if username and password else f"{username}@{parsed.hostname}" if username else parsed.hostname
        if parsed.port:
            netloc += f":{parsed.port}"
        
        return urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
    return uri

# Create MongoDB client
mongodb_uri = os.getenv("MONGODB_URI")
encoded_uri = encode_mongodb_uri(mongodb_uri) if mongodb_uri else mongodb_uri

client = AsyncIOMotorClient(
    encoded_uri,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

# Get database
db = client[os.getenv("MONGODB_DB_NAME")]

# Collections
patients_collection = db["patient"]

async def connect_to_mongo():
    """Connect to MongoDB and verify connection."""
    try:
        await client.admin.command('ping')
        print(f"Connected to MongoDB: {os.getenv('MONGODB_DB_NAME')}")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close MongoDB connection."""
    client.close()
    print("Closed MongoDB connection")