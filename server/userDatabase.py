import motor.motor_asyncio
import urllib
from bson.objectid import ObjectId

MONGO_HOST = MONGODB_HOST
#MONGO_PORT = "27017"
MONGO_DB = DB_NAME
MONGO_USER = MONGO_DB_USERNAME
MONGO_PASS = MONGO_DB_PASSWORD

uri = "mongodb+srv://{}:{}@{}/{}?authSource=admin".format(MONGO_USER,MONGO_PASS, MONGO_HOST, MONGO_DB)


client = motor.motor_asyncio.AsyncIOMotorClient(uri)

database = client["UserDB"]

def user_helper(user)-> dict:
    return {
        "id":str(user["_id"]),
        "name": user["name"],
        "mob_no": user["mob_no"],
        "date_of_registration": user["date_of_registration"],
        "valid_till": user["valid_till"],
        
        "device_id": user["device_id"],
        "device_name": user["device_name"]
        }

def admin_helper(admin)->dict:
    return {
        "id":str(admin["_id"]),
        "name": admin["name"],
        "password": admin["password"],
        "mob_no":admin["mob_no"]
}


#   Add New User
async def add_user(user_data: dict) -> dict:
    user_collection = database.get_collection("User Details")
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user) 



## Update User

async def update_user(id:str,data:dict):
    user_collection = database.get_collection("User Details")
    user_document = await user_collection.find_one({"_id": ObjectId(id)})
    if len(data) < 1:
        return False
    if user_document:
        updated_user_data = await user_collection.update_one(
         {"_id": ObjectId(id)}, {"$set":data}   
        )
        if updated_user_data:
            return True
        else:
             False        


#retrieve all users
async def retrieve_all_users():
    user_collection = database.get_collection("User Details")
    user_ = []
    async for user in user_collection.find():
        user_.append(user_helper(user))
    return user_

# retreve one user
async def retrieve_user(mob_no: int) -> dict:
    user_collection = database.get_collection("User Details")
    user = await user_collection.find_one({"mob_no": mob_no})
    if user:
        return user_helper(user)


# Delete User 
async def delete_user(id: str):
    user_collection = database.get_collection("User Details")
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True



    ############## Admin Database ################
# Get All Admin Details
async def get_All_Admins():
    admin_collection = database.get_collection("Admin Details")
    admin_ = []
    async for admin in admin_collection.find():
        admin_.append(admin_helper(admin))
    return admin_


async def increment_admin():
    login_collection = database.get_collection("LoginInfo")
    document = await login_collection.find_one({"_id": ObjectId("6075881d663c50b375f2d583")})
    value=document["no_of_admin_logins"]
    value=value+1
    if(value<5):
        data_dict = {
            "no_of_admin_logins": value
        }
        updated_login = await login_collection.update_one({"_id": ObjectId("6075881d663c50b375f2d583")},{"$set":data_dict})
        if updated_login:
            return True
    else:
        return False

async def decrement_admin():
    login_collection = database.get_collection("LoginInfo")
    document = await login_collection.find_one({"_id": ObjectId("6075881d663c50b375f2d583")})
    value=document["no_of_admin_logins"]
    value=value-1
    data_dict = {
        "no_of_admin_logins": value
        }
    updated_login = await login_collection.update_one({"_id": ObjectId("6075881d663c50b375f2d583")},{"$set":data_dict})
    if updated_login:
        return True
    else: 
        return False
              