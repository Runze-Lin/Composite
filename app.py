from fastapi import FastAPI, Request, HTTPException
import mysql.connector
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# URLs for each microservice
USERS_SERVICE_URL = 'http://ec2-3-144-182-9.us-east-2.compute.amazonaws.com:8012'
PROPERTIES_SERVICE_URL = 'https://e6156-i-am-bezos-402423.ue.r.appspot.com'
BOOKINGS_SERVICE_URL = 'ec2-13-59-140-159.us-east-2.compute.amazonaws.com:8012'

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return FileResponse('static/index.html')

@app.get("/properties")
async def get_properties(property_id: Optional[str] = None, first_name: Optional[str] = None,
                         last_name: Optional[str] = None, property_address: Optional[str] = None,
                         house_type: Optional[str] = None, house_size: Optional[int] = None,
                         size_gt: Optional[int] = None,
                         size_lt: Optional[int] = None,
                         price: Optional[int] = None,
                         price_gt: Optional[int] = None,
                         price_lt: Optional[int] = None, availability: Optional[bool] = None, 
                         host_id: Optional[str] = None, limit: Optional[int] = None, 
                         offset: Optional[int] = None):
    params = {
        "property_id": property_id,
        "first_name": first_name,
        "last_name": last_name,
        "property_address": property_address,
        "house_type": house_type,
        "house_size":house_size,
        "size_gt": size_gt,
        "size_lt": size_lt,
        "price":price,
        "price_gt": price_gt,
        "price_lt": price_lt,
        "availability": availability,
        "host_id": host_id,
        "limit": limit,
        "offset": offset
    }
    response = requests.get(PROPERTIES_SERVICE_URL + '/properties', params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from User Service")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
