from fastapi import FastAPI
from fastapi.responses import JSONResponse
from client import collection_name


# This is used to run our FastAPI Server 
# uvicorn fast:app --reload --port=8000 --host=127.0.0.1  

# --------------------- FAST API Application ------------------------ 
app = FastAPI()

# Perform READ update request to obtain the excel file 
@app.get("/")
async def getExcel(fileToFind: dict):

    file_to_find = fileToFind.get('file_name')

    document = collection_name.find_one({'xlsx_name': file_to_find})

    if document is None:
        data = {"message": "Document Not Found"}
        return JSONResponse(content=data, status_code=404)
    
    # We have found the document and only want to send specific data back to the client 
    document_path = {"message": "Successfully Retrieved The XLSX File!", "xlsx_file_path": document.get('xlsx_file'), "xlsx_file_info": document.get("xlsx_file_info")}
    return JSONResponse(content=document_path, status_code=200)
    

# POST request to push the excel resource
@app.post("/")
async def pushExcel(excelInfo: dict):

    file_name = excelInfo.get('file_name')
    file = excelInfo.get('file')
    file_info_buffer = excelInfo.get('file_info_buffer')

    # Check to see such a file already exists in the database
    existing_document = collection_name.find_one({'xlsx_name': file_name})

    if existing_document:
        data = {"message": "The file already exists! A request to UPDATE the file will be displayed"}
        return JSONResponse(content=data, status_code=500)
    else:
        
        # The file does not exist so we make it 
        transcript_xlsx_dict = {'xlsx_name': file_name, 'xlsx_file': file, 'xlsx_file_info': file_info_buffer}
    
        # Insert into the database 
        try: # Await is not needed here but important to have try-catch
            collection_name.insert_one(transcript_xlsx_dict)
            data = {"message": "Transcript was successfully made"}
            return JSONResponse(content=data, status_code=200)
        except:
            data = {"message": "Error in creating transcript"}
            return JSONResponse(content=data, status_code=500)
    
# Might need to come back here in order to fix this method but we will do this at the end 
@app.put("/")
async def updateExcel(excelInfo: dict):

    file_name = excelInfo.get('file_name')
    file = excelInfo.get('file')
    file_info_buffer = excelInfo.get('file_info_buffer')

    # Our Filter criteria
    filter_criteria = {'xlsx_name': file_name}

    # Our Update operation
    update_operation = {"$set": {'xlsx_name': file_name, 'xlsx_file': file, 'xlsx_file_info': file_info_buffer}}

    # Our filter criteria is simply finding the document with the existing file name
    update_existing_document = collection_name.update_one(filter_criteria, update_operation)

    if update_existing_document.modified_count > 0:
        data = {"message": "The document has been sucessfully updated!"}
        return JSONResponse(content=data, status_code=200) 
    else:
        data = {"message": "The document is already up-to-date"}
        return JSONResponse(content=data, status_code=500)


# Will be implemented soon 
@app.delete("/")
async def deleteExcel(fileToDelete: dict):

    file_to_find = fileToDelete.get('file_name')

    document = collection_name.find_one({'xlsx_name': file_to_find})

    if document is None:
        data = {"message": "Document Not Found"}
        return JSONResponse(content=data, status_code=404)
    else:

        collection_name.delete_one({'xlsx_name': file_to_find})
        data = {"message": "Document Successfully Deleted!"}
        return JSONResponse(content=data, status_code=200)