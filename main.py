import uvicorn
import asyncio
import os
import time


os.environ['TZ'] = 'Asia/Kolkata' # set new timezone
time.tzset()

    

    



if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)


    

