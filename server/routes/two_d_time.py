from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_time,
    retrieve_alltime,
    retrieve_time,
    update_time,
    delete_time
)
from server.models.twod_time import (
    ErrorResponseModel,
    ResponseModel,
    TwoD_Schema,
    Update2D_Model
)

router = APIRouter()

@router.post("/", response_description="2d data added into the database")
async def add_twod_data(twod_data: TwoD_Schema = Body(...)):
    twod_data = jsonable_encoder(twod_data)
    new_twod_data = await add_time(twod_data)
    return ResponseModel(new_twod_data, "two_d_data added successfully.")

@router.get("/{date}/{series}", response_description="twod_data retrieved")
async def get_alltime_2d_data(date:str,series:int):
    time_ = await retrieve_alltime(date,series)
    if time_:
        return ResponseModel(time_, "All 2d data for time till now retrieved")
    return ResponseModel(time_, "Empty list returned")

@router.get("/{datee}/", response_description="2d data retrieved for given id")
async def get_twod_data(datee,timee):
    timee = await retrieve_time(datee,timee)
    if timee:
        return ResponseModel(timee, "2d data retrieved successfully")
        
    return ErrorResponseModel("An error occurred.", 404, "2d data doesn't exist.")


@router.put("/{date}/{time}")
async def update_twod_data(date: str,time: str, req: Update2D_Model = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_twod_value = await update_time(date,time, req)
    if updated_twod_value:
        return ResponseModel(
            "Time value for date  {} and time {} has been updated".format(date,time),
            "Time data Updated Successfully"
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the time data.",
    )    