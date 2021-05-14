from fastapi import FastAPI
from server.routes.two_d_time import router as twod_router

from server.routes.user import router as user_router


app = FastAPI()

app.include_router(twod_router, tags=["2d_data"], prefix="/2d_data")

app.include_router(user_router, tags=["UserData"],prefix="/users")






@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}








