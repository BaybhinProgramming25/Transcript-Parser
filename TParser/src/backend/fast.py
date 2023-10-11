from fastapi import FastAPI
from mongo import collection_name

app = FastAPI()

# Perform READ update request to obtain the csv file 
@app.get("/")
async def getExcel():
    print("Hello World")

# POST request to push the excel resource
@app.post("/")
async def pushExcel(excelInfo: dict):

    # We get the file 
    file_name = excelInfo.get('file_name')
    file = excelInfo.get('file')

    transcript_xlsx_dict = {'xlsx_name': file_name, 'xlsx_file': file}

    # Insert into the database 
    try: # Await is not needed here but important to have try-catch
        collection_name.insert_one(transcript_xlsx_dict)
        return True 
    except Exception as e:
        print(f'Error in inserting data {e}')
        return False 
    
@app.put("/")
async def updateExcel(excelInfo: dict):
    print("TO BE IMPLEMENTED")

@app.delete("/")
async def deleteExcel(excelInfo: dict):
    print("TO BE IMPLEMENTED")
    # We delete a specific excel file 

