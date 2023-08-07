#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# FAST API PACKAGES
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
from fastapi import FastAPI
from pydantic import BaseModel

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# INTERNAL MANAGEMENT CLASSES
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
from CLASSES.MPOD_library import MPOD
from CLASSES.MPOD_library import UNIT
from CLASSES.dictionary import classes_dictionary
import json, time

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# GENERATING OBJECT MODELS
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# Reading modules JSON file
with open('CONFIG/modules_units.json', "r") as json_file:
    moduleDB = json.load(json_file)

# Reading other units JSON file
with open('CONFIG/others_units.json', "r") as json_file:
    othersDB = json.load(json_file)

# Get list of units  attached to modules
id = 0
attached_units_dict = {}
for module in moduleDB.keys():
    unit_names = moduleDB[module].keys()
    for unit in unit_names:
        kind = moduleDB[module][unit]["class"]
        object = classes_dictionary[kind]
        attached_units_dict[id] = object(module, unit, moduleDB[module][unit])
        id += 1

id = 0
others_dict = {}
# Get list of units not attached to modules
for unit in othersDB.keys():
    kind = othersDB[unit]["class"]
    object = classes_dictionary[kind]
    others_dict[id] = object(None, unit, othersDB[unit])
    id += 1

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# FAST API CONFIGURATION
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# FastAPI handles JSON serialization and deserialization for us.
app = FastAPI()

#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# GET METHODS
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
@app.get("/")
def index():
    return {"message" : "Hello World!"}

@app.get("/allmodules")
def get_ModulesJSON():
    '''
    Return modules JSON file
    '''
    return moduleDB

@app.get("/allothers")
def get_other_modulesJSON():
    '''
    Return other units (i.e. Gizmo) JSON file
    '''
    return othersDB

@app.get("/attached_units")
def get_attached_units():
    '''
    Return all objects of units connected to modules
    '''
    return attached_units_dict

@app.get("/attached_units/{unit_id}")
def get_attached_unit_by_id(unit_id: int):
    '''
    Return object by id
    '''
    return attached_units_dict[unit_id]

@app.get("/other_units")
def get_other_units():
    '''
    Return all objects of units NOT connected to modules
    '''
    return others_dict

@app.get("/other_units/{unit_id}")
def get_others_by_id(unit_id: int):
    '''
    Return object by id
    '''
    return others_dict[unit_id]

@app.get("/attached_units/{unit_id}/status")
def get_attached_status_by_id(unit_id: int):
    '''
    Return unit status of measuring elements (i.e. {light, current, rtd})
    '''
    return attached_units_dict[unit_id].getMeasuringStatus()

@app.get("/other_units/{unit_id}/status")
def get_other_status_by_id(unit_id: int):
    '''
    Return other unit status (i.e. {light, current, rtd})
    '''
    return others_dict[unit_id].getCrateStatus()
    
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
# PUT METHODS
#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
@app.put("/attached_units/{unit_id}/{measuring}/turn-on")
def turnON_attached_by_id(unit_id: int, measuring: str):
    '''
    Turn on measuring from unit connected to module (i.e. light readout from MPOD)
    '''
    attached_units_dict[unit_id].powerON(measuring)
    return {"message" : attached_units_dict[unit_id].getOnMessage()} 

@app.put("/attached_units/{unit_id}/{measuring}/turn-off")
def turnOFF_attached_by_id(unit_id: int, measuring: str):
    '''
    Turn off measuring from unit connected to module (i.e. light readout from MPOD)
    '''
    attached_units_dict[unit_id].powerOFF(measuring)
    return {"message" : attached_units_dict[unit_id].getOffMessage()} 

@app.put("/other_units/{unit_id}/turn-on")
def turnON_other_by_id(unit_id: int):
    '''
    Turn on unit NOT connected to module (i.e. MPOD Crate)
    '''
    others_dict[unit_id].powerSwitch(1)
    return {"message" : others_dict[unit_id].getOnMessage()} 
    
@app.put("/other_units/{unit_id}/turn-off")
def turnOFF_other_by_id(unit_id: int):
    '''
    Turn off unit NOT connected to module (i.e. MPOD Crate)
    '''
    others_dict[unit_id].powerSwitch(0)
    return {"message" : others_dict[unit_id].getOffMessage()} 