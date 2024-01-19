# app/database.py
from pymongo import mongo_client
import pymongo
from decouple import config

print(config("DATABASE_URL"))
client = mongo_client.MongoClient(config("DATABASE_URL"))
print("Connected to MongoDB...")

db = client[config("MONGO_INITDB_DATABASE")]
Otp = db.otp
Otp.create_index([("username", pymongo.ASCENDING)], unique=True)