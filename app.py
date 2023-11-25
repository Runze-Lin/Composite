from fastapi import FastAPI, Request, HTTPException
from composites import Composite
from fastapi.responses import JSONResponse, HTMLResponse
import mysql.connector
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import random
import time
import aiohttp
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
composite = Composite()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# API Endpoints

@app.get("/")
async def root():
    return FileResponse('static/index.html')

# sync and async aggregators for sprint 2
@app.get("/sync-aggregator")
async def sync_aggregator():
    result = composite.fetch_sync()
    return JSONResponse(content={"result": result})

@app.get("/async-aggregator")
async def async_aggregator():
    result = await composite.fetch_async()
    return JSONResponse(content={"result": result})

@app.get("/properties")
async def get_properties(property_id: Optional[str] = None, property_address: Optional[str] = None,
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
        "property_address": property_address,
        "house_type": house_type,
        "house_size": house_size,
        "size_gt": size_gt,
        "size_lt": size_lt,
        "price": price,
        "price_gt": price_gt,
        "price_lt": price_lt,
        "availability": availability,
        "host_id": host_id,
        "limit": limit,
        "offset": offset
    }
    properties_data = composite.get_properties(params)
    return properties_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
