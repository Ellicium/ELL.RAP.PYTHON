import logging
import os

from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks

from io import BytesIO
from typing import Optional
import requests

from ..config.db_config import database
from ..services.data_service import load_data
# upload_bom_function,upload_po_function,upload_cost_breakdown_function,upload_material_breakdown_function

router = APIRouter()

#---------------------------------RAP
#RAP


@router.post("/data/api_data_load", tags=["data"])
async def load_data_tables(file: UploadFile = File(...)):
    try:
        dbobj=database()

        contents = await file.read()

        # Convert binary to a file-like object
        excel_file = BytesIO(contents)
        
        flag = load_data(dbobj,excel_file)
        
        true_response={'response_code':200,'Message':'Tables Updated Successfully'}
        false_response={'response_code':400,'Message':'Tables Not Updated Please Try Again'}
                
        if flag==True:
            return JSONResponse(true_response,status_code=true_response['response_code'])
        return JSONResponse(false_response,status_code=false_response['response_code'])
    except Exception as e:
        logger.error("print_input failed", exc_info=e)
        return JSONResponse(f"error {e}", status_code=500)

