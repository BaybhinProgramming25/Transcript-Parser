from pymongo import MongoClient

# --------------------- MongoDB database ------------------------ #
# Create MongoDB client
client = MongoClient('mongo', 27017)

# Determine name of database 
db = client["ExcelTranscripts"]

# Determine collection name within our database
collection_name = db["ExcelSheets"]