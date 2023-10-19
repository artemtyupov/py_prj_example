# server.py

import logging
import sys
from typing import List, Union

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse

sys.path.append(".")
sys.path.append("..")

from utils import get_excel_data, get_updated_excel_data, validate_excel_data

from shared_files.models import CClientSpending, CRealPriceItem

app = FastAPI()

# Настройка логирования
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO)

@app.post("/validate_excel_data")
async def process(user_client_id: int, type: str, new_file_data: UploadFile):
    try:
        return await validate_excel_data(user_client_id, type, await new_file_data.read())
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/get_updated_excel_data")
async def process(user_client_id: int, type: str, new_file_data: UploadFile, old_models:  List[Union[CClientSpending, CRealPriceItem]] = None):
    try:
        return await get_updated_excel_data(user_client_id, type, await new_file_data.read(), old_models)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/get_excel_data")
async def process(user_client_id: int, type: str, old_models: List[Union[CRealPriceItem, CClientSpending]] = None):
    try:
        filepath = await get_excel_data(user_client_id, type, old_models)
        return FileResponse(path=filepath)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8005)