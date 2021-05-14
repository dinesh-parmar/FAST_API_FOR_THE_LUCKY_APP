from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.userDatabase import (
    add_user,
    retrieve_all_users,
    retrieve_user,
    delete_user,
    get_All_Admins,
    increment_admin,
    decrement_admin,
    update_user
)
from server.models.users import (
    ErrorResponseModel,
    ResponseModel,
    User_Schema,
    Update_User_Model,
    Register_Phone
)

router = APIRouter()

## Admin User Information update
@router.put("/update/{id}",response_description= "User Data Updated by the admin ")
async def update_user_data(id:str, user_data: Update_User_Model=Body(...)):
    req = {k: v for k, v in user_data.dict().items() if v is not None}
    updateUserDataResponse = await update_user(id, req)
    if updateUserDataResponse:
        return ResponseModel(
            "User data with {} updated successfully".format(id),
            "User data Updated Successfully"
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )

## Register the device from the Customer
@router.put("/registerDevice/{id}",response_description="Device Registered Successfully")
async def register_device(id:str, device_data: Register_Phone=Body(...) ):
    req = {k: v for k, v in device_data.dict().items() if v is not None}
    updateUserDataResponse = await update_user(id, req)
    if updateUserDataResponse:
        return ResponseModel(
            "Done", "Device Registered Successfully"
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )



@router.post("/", response_description="User Data added into the database")
async def add_user_data(user_data: User_Schema = Body(...)):
    user_data = jsonable_encoder(user_data)
    new_data = await add_user(user_data)
    return ResponseModel(new_data, "User Details added successfully.")

@router.get("/", response_description="User Data retrieved")
async def get_all_users():
    user_ = await retrieve_all_users()
    if user_:
        return ResponseModel(user_, "All User data retrived successfully")
    return ResponseModel(user_, "Empty list returned")

@router.get("/{mob_no}", response_description="User Data retrieved")
async def get_user(mob_no:int):
    user_ = await retrieve_user(mob_no)
    if user_:
        return ResponseModel(user_, "User Data retrieved Successfully")
    return ResponseModel(user_, "Empty list returned")


@router.delete("/{id}",response_description="User Data Deleted from the database")
async def delete_user_with_id(id:str):
    deleted_user = await delete_user(id)
    if(deleted_user):
        return ResponseModel(deleted_user,"User with "+str(id)+"has been deleted")
    return ErrorResponseModel("An error occurred", 404, "User with id {0} doesn't exist".format(id))    


@router.get("/admin/",response_description="Admin Data retrieved successfully")
async def get_all_admin():
    allAdmins_ = await get_All_Admins()
    if allAdmins_:
        return ResponseModel(allAdmins_, "All Admin data retrived successfully")
    return ResponseModel(allAdmins_, "Empty list returned")   


@router.get("/loginInfo/",response_description="Login Admin Incremented Successfully")
async def increment_admins():
    updated_login = await increment_admin()
    if updated_login:
        return ResponseModel(updated_login, "Incremented Successfully")
    return ResponseModel(updated_login,"Incremented Successfully")    


@router.get("/logout/",response_description="Logged out  Successfully")
async def logout():
    updated_logout = await decrement_admin()
    if updated_logout:
        return ResponseModel(updated_logout,"Logged out successfully")
    return ResponseModel(updated_logout,"Logged out successfully")   
