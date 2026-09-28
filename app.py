# ECSE3038 - Week 4, Lecture 1 - starter
# Monday's API with the hard-coded list emptied.
# Run:  uvicorn app:app --reload
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import ASCENDING
from pymongo.errors import DuplicateKeyError

import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()                                                  #loads the .env file
#print(os.getenv("MONGODB_URI"))                                             
client = MongoClient(os.getenv("MONGODB_URI"))                 #uses this line to conenct to Mongo DB cluster
db = client["ecse3038"]                                        #database is cl
devices = db["devices"] 

devices.create_index([("name", ASCENDING)], unique=True)

app = FastAPI()



class Device(BaseModel):
    name: str
    room: str
    temp: float
    online: bool


readings = []


@app.get("/devices")
def get_devices():
    return list(devices.find({}, {"_id": 0}))   #{}means we want every part of the object, {"_id": 0} means that we don't want the "_id" field


@app.get("/devices/{name}")
def get_device(name: str):
    device = devices.find_one({"name": name}, {"_id": 0})
    if device is None:
        raise HTTPException(status_code=404, detail="No device called " + name)
    return device


@app.post("/devices", status_code=201)
def create_device(device: Device):
    new_device = device.model_dump()
    try:
        devices.insert_one(new_device)    
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail=f"A device named '{device.name}' already exists."
        )
    new_device.pop("_id")
    return new_device

"""
@app.put("/devices/{name}")
def put_device(name: str, updated_device: Device):
    for index, device in enumerate(readings):   
        if device["name"] == name:   
            updated_device = devices.find_one({"name": name}, {"_id": 0})             
            readings[index] = updated_device.model_dump()  
            return readings[index]
    raise HTTPException(status_code=404, detail="No device called " + name)


@app.delete("/devices/{name}")
def delete_device(name: str):
    for device in readings:                    
        if device["name"] == name:                 
            readings.remove(device)
            return {"deleted" : name }
    raise HTTPException(status_code=404, detail = f"No device called {name}")
"""


