import motor.motor_asyncio
import urllib
from bson.objectid import ObjectId
from datetime import datetime

MONGO_HOST = "cluster0.tbcp3.mongodb.net" 
#MONGO_PORT = "27017"
MONGO_DB = "date"
MONGO_USER = "dinesh"
MONGO_PASS = urllib.parse.quote("dpp@1999@")

uri = "mongodb+srv://{}:{}@{}/{}?authSource=admin".format(MONGO_USER,MONGO_PASS, MONGO_HOST, MONGO_DB)
MONGO_DETAILS = "mongodb+srv://dinesh:"+urllib.parse.quote("dpp@1999@")+"@cluster0.tbcp3.mongodb.net/date?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(uri)

database = client["2ddate"]



def twod_helper(date) -> dict:
    return {
        "id":str(date["_id"]),
        "time": date["time"],
        "twod_value": date["twod_value"],
        "fourd_value": date["fourd_value"]
        }


def whole_day_twod_helper(date,series) -> dict:
    return {
        "id":str(date["_id"]),
        "time": date["time"],
        "twod_value": date["twod_value"][series],
        "fourd_value": date["fourd_value"][series]
        }


#add a time to our 2d database
async def add_time(time_data: dict) -> dict:
    date_collection = database.get_collection("26-03-2021")
    timee = await date_collection.insert_one(time_data)
    new_timee = await date_collection.find_one({"_id": timee.inserted_id})
    return twod_helper(new_timee)      

#retrieve all time
async def retrieve_alltime(date:str,series: int):
    #x= datetime.now()
    #today_date = str(x.day).zfill(2)+"-"+str(x.month).zfill(2)+"-"+str(x.year)
    date_collection = database.get_collection(date)
    time_ = []
    async for timee in date_collection.find():
        time_.append(whole_day_twod_helper(timee,series))
    return time_ 

# Retrieve a time value with Id
async def retrieve_time(date: str,timee: str) -> dict:
    date_collection = database.get_collection(date)
    timee = await date_collection.find_one({"time":timee})
    if timee:
        return twod_helper(timee)

# Update a 2d_data with the matching id
async def update_time(date:str, time: str, data: dict):
    date_collection = database.get_collection(date)
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    timee = await date_collection.find_one({"time": time})
    if timee:
        updated_time = await date_collection.update_one(
            {"time" : time}, {"$set": data}
        )
        if updated_time:
            return True
        return False     

# Delete a two_data from the database
async def delete_time(id: str):
    date_collection = database.get_collection("26-03-2021")
    timee = await date_collection.find_one({"_id": ObjectId(id)})
    if timee:
        await date_collection.delete_one({"_id": ObjectId(id)})
        return True


