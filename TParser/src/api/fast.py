from fastapi import FastAPI, UploadFile
from pydantic import BaseModel


class Item(BaseModel):
    id: int 
    name: str 

# Out first api 
app = FastAPI() 

# Keep a list of the items we want to add 
inventory = []

# Make a simple POST request
@app.post("/excel/")
def makeStringPost(item: Item):

    # FastAPI validates the data being sent but WHY THE FUCK IS IT NOT DOING THAT? 
    print (item) # Check to see if this is the item 
