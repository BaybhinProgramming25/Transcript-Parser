from pymongo import MongoClient

# Create MongoDB client
client = MongoClient("mongodb://localhost:27017")

# Determine name of database 
db = client["ExcelTranscripts"]

# Determine collection name within our database
collection_name = db["ExcelSheets"]