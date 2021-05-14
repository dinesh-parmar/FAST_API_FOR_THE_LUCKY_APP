from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ValidationError


class User_Schema(BaseModel):
    name: str = Field(...)
    mob_no: int = Field(...)
    date_of_registration : str = Field(...)
    device_id: str = Field(...)
    valid_till: str = Field(...)
    device_name: str = Field (...)

    class Config:
        schema_extra={
            "name": "Name Surname",
            "mob_no": "1234567890",
            "date_of_registration": "01-04-2021",
            "device_id": "12345678",
            "valid_till" : "2021-05-29T18:30:00.000+00:00",
            "device_name": "Samsung"
            
        }

        
class Update_User_Model(BaseModel):
    name: str = Field(...)
    mob_no: int = Field(...)
    device_id: str = Field(...)
    valid_till: str = Field(...)
    device_name: str = Field(...)

    class Config:
        schema_extra={
            "name": "Name Surname",
            "mob_no": "1234567890",
            "device_id": "12345678",
            "valid_till" : "2021-05-29T18:30:00.000+00:00",
            "device_name": "Samsung"
        }

class Register_Phone(BaseModel):
    device_id: str = Field(...)
    device_name: str = Field(...)

    class Config:
        schema_extra={
            "device_id": "12345678",
            "device_name": "Samsung"
        }        


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }
def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}



