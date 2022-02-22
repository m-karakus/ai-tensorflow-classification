import asyncio
from datetime import datetime
import uvicorn
from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
import json
from producer import main as producer
import threading
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["https://www.kizlarsoruyor.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def async_get_data(request):
    data = request.json
    sonuc = await producer(data)
    # print(json.dumps(data, indent=4))
    return 

@app.get("/")
async def get_data(request: Request):
    try:
        data = await request.json()
        data['timestamp']=datetime.now().isoformat()
        # print(json.dumps(data, indent=4))
        
        t = threading.Thread(target=producer,  args=(data,))
        t.start()
        return data

    except Exception as e:
        return "you have to send body and you have to use GET or POST"

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0", port=22009)