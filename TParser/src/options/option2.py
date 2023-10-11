# GET an XLSX fie 

from backend.mongo import collection_name
import requests 

def option2():
    
    # We then want to list out all of the transcripts that are currently stored on the database 
    # We will then ask the user the user to select which of these transcripts to get 
    # Once the user selects, the transcript will be in the folder

    # If there are no documents, then print a message saying that the user must need to create a document first 

    database_documents = collection_name.find()

    for document in database_documents:
        print(document, end="\n\n")

    