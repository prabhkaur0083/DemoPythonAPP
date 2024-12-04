from database.dbConnection import MongoDBConnection
from core.models.report.ResultModel import Result
from pymongo.errors import DuplicateKeyError
from pymongo import errors
from datetime import datetime


class MongoDBHandler:
    def __init__(self):
        connection = MongoDBConnection()
        self.db = connection.get_database()

    # Insert the Document from the Collection
    def insertDocument(self, collection_name: str, data: dict) -> Result:
        try:
            collection = self.db[collection_name]
            collection.insert_one(data)
            message = f"Document successfully inserted into {collection_name}: {data}"
            return Result(Data=data, Status=1, Message=message)

        except DuplicateKeyError as dup_ex:
            message = f"Duplicate key error inserting document into {collection_name}: {dup_ex}"
            print(f"{datetime.now()} {message}")
            return Result(Status=2, Message=message)

        except Exception as ex:
            message = (
                f"Error inserting document into {collection_name} in InsertQuery: {ex}"
            )
            print(f"{datetime.now()} {message}")
            return Result(Status=0, Message=message)

    # Insert The Multiple Documents
    def insertDocuments(self, collectionName: str, dataList: list) -> Result:
        try:
            collection = self.db[collectionName]
            collection.insert_many(dataList)

            return Result(
                Status=1,
                Message=f"Documents successfully inserted into {collectionName}",
            )

        except errors.BulkWriteError as bwe:
            errorMessages = []
            for error in bwe.details["writeErrors"]:
                errorMessages.append(
                    f"Error at index {error['index']}: {error['errmsg']}"
                )
            print(f"{datetime.now()} Duplicacy is Occur ")
            return Result(Status=2, Message=str(errorMessages))

        except Exception as ex:
            message = f"Error inserting documents into {collectionName}: {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Status=0, Message=message)

    # Load The All Documents From Collection
    def loadAllDocument(self, collection_name: str) -> Result:
        try:
            collection = self.db[collection_name]
            documents = list(collection.find())
            return Result(
                Data=documents,
                Status=1,
                Message=f"Documents successfully retrived into {collection_name}",
            )

        except Exception as ex:
            message = f"Error in Loading documents from {collection_name}: {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Status=0, Message=message)

    # Load the one Document From Collection
    def findDocument(self, collection_name: str, query: dict) -> Result:
        try:
            collection = self.db[collection_name]
            document = collection.find_one(query)
            return Result(
                Data=document,
                Status=1,
                Message=f"Documents successfully retrived into {collection_name}",
            )

        except Exception as ex:
            message = f"Error in Finding document from {collection_name}: {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Status=0, Message=message)

    # Load the Multiple Documents From Collection based on Query
    def findDocuments(self, collection_name: str, query: dict):
        try:
            collection = self.db[collection_name]
            documents = list(collection.find(query))
            return Result(
                Data=documents,
                Status=1,
                Message=f"Documents successfully retrived from {collection_name}",
            )

        except Exception as ex:
            message = f"Error in Finding documents from {collection_name}: {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Status=0, Message=message)

    # Updated the Document from the Collection
    def update_document(self, collection_name: str, query: dict, new_values: dict):
        try:
            collection = self.db[collection_name]
            collection.update_one(query, {"$set": new_values})
            return Result(
                Status=1, Message=f"Document successfully Updated in {collection_name}"
            )

        except Exception as ex:
            message = f"Error while while updating the {collection_name}: {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Status=0, Message=message)

    # Delete The dcoument from Collection
    def deleteDocument(self, collection_name: str, query: dict) -> Result:
        try:
            collection = self.db[collection_name]
            collection.delete_one(query)
            return Result(
                Status=1,
                Message=f"Document deleted successfully from {collection_name} where {query}",
            )

        except Exception as ex:
            message = f"Error deleting document from {collection_name}: {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Status=0, Message=message)

    # Search Document Based on Id
    def SearchId(self, collectionName: str, documentId: int) -> Result:
        try:
            collection = self.db[collectionName]
            document = collection.find_one({"_id": documentId})
            if document:
                return Result(
                    Status=1,
                    Message=f"Document Found with  successfully with given ID from {collection}",
                )
            else:
                return Result(
                    Status=1,
                    Message=f"Document with {documentId} not  Found in  {collection}",
                )

        except Exception as ex:
            message = f"Error while while updating the {collectionName}: {ex}"
            print(f"{datetime.now()} {message}")
            return Result(Status=0, Message=message)

    def getCollection(self, collection_name: str):
        try:
            return self.db[collection_name]
        except Exception as ex:
            message = f"Error while getting the collection '{collection_name}': {ex}"
            print(f"{datetime.now()} {message}")
            raise Exception(message)
