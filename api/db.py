import motor.motor_asyncio
from dotenv import dotenv_values

config = dotenv_values("./.env")


client = motor.motor_asyncio.AsyncIOMotorClient(config["MONGO_DB_CONNECTION_URI"])
db = client.googleTranslate
