import os
import motor.motor_asyncio

MONGO_DETAILS = os.environ.get("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
collection = client.titanic.people
