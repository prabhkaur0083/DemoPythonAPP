import pymongo
from dotenv import load_dotenv
import os

load_dotenv()


class MongoDBConnection:
    username = os.getenv("DATABASE_USERNAME")
    password = os.getenv("DATABASE_PASSWORD")
    # Static URL and database name
    url = f"mongodb+srv://{username}:{password}@cluster0.kyurv.mongodb.net/?authSource=admin"
    # dbName = "InfinVersion2"
    dbName = "InfinDb"

    def __init__(self, uri: str = url, dbName: str = dbName):
        """Initializes the MongoDB connection."""
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[dbName]

    def get_database(self):
        """Returns the database instance."""
        return self.db
