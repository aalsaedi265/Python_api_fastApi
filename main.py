import fastapi
from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    stand:str
    occupation: Optional[str] = None
    
    
class Update(BaseModel):
    name:Optional[str] = None
    stand:Optional[str] = None
    occupation: Optional[str] = None


@app.get("/")
def about():
    return {"Dio": "The world"}

inventory = {
    # 1:{
    #     "name": "Funny Valentine",
    #     "stand": "Dirty dees done dirty Cheep",
    #     "occupation": "president of USA"
    # }
}
# http://127.0.0.1:8000/get-item/1

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(...,description="the ID of the item you would like to view")):
    return inventory[item_id]

# http://127.0.0.1:8000/get-by-name?name=Funny Valentine

@app.get("/get-by-name")
#none are optional aquagemtns be sure put arugemtn second to mandatory one
def get_by_name(name:Optional[str] = None ):
    
    for item_id in inventory:
        if inventory[item_id].name == name :
            return inventory[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.post("/create-itme/{item_id}")
def create_item( item_id: int ,item: Item):
    if item_id in inventory:
        return {"Error":"item already exists"}
    inventory[item_id] = item
    # inventory[item_id]={ 
    #                     "name":item.name,
    #                     "stand": item.stand,
    #                     "occupation": item.occupation
    #                     }
    return inventory[item_id]

@app.put("/update-itme/{item_id}")
def update_item(item_id:int , item: Update):
    if item_id not in inventory:
        return {"Error":"item does not exists"}
    if item.name != None:
        inventory[item_id] = item.name
        
    if item.stand != None:
        inventory[item_id] = item.stand
                
    if item.occupation != None:
        inventory[item_id] = item.occupation 
        
           
    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int= Query(..., description= "ID of the item to delete",gt=0)):
    if item_id not in inventory:
        return {"error": " ID does not "}
    del inventory[item_id]
    return {"success": True}