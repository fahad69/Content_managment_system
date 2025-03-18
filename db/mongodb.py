"""
MongoDB connection setup using Motor.
"""

import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://admin:admin@buddhatv.c1vxx.mongodb.net/?retryWrites=true&w=majority&appName=buddhatv"
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.cms_db

# Define collections for websites and blogs.
website_collection = database.get_collection("websites")
blog_collection = database.get_collection("blogs")
