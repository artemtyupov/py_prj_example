import logging
import os
from typing import List, Union

import httpx

from shared_files.models import CClientSpending, CRealPriceItem

if os.getenv('IS_DOCKER') == "1":
    HOST = "excel_service_container"
else:
    HOST = "localhost"

async def get_updated_excel_data(user_client_id: int, type: str, filepath, old_models: Union[List[CClientSpending], List[CRealPriceItem]] = None) -> Union[List[CClientSpending], List[CRealPriceItem]]:
    with open(filepath, 'rb') as filedata:
        async with httpx.AsyncClient() as client:
            params = {
                "user_client_id" : user_client_id,
                "type" : type,
            }
            
            json_data = {}
            if old_models:
                json_data = [model.model_dump() for model in old_models]
            
            response = await client.post(f"http://{HOST}:8005/get_updated_excel_data", 
                                         params=params,
                                         json=json_data,
                                         files={"new_file_data" : (filepath, filedata)}, 
                                         timeout=60)
            
            if response.status_code != 200:
                logging.error(response.text)
            
            retval_objs = []
            for model in response.json():
                if type == "other_spendings":
                    retval_objs.append(CClientSpending.model_validate(model))
                else:
                    retval_objs.append(CRealPriceItem.model_validate(model))
                    
            return retval_objs
    
async def get_excel_data(user_client_id: int, type: str, old_models: Union[List[CClientSpending], List[CRealPriceItem]] = None):
    async with httpx.AsyncClient() as client:
        params = {
            "user_client_id" : user_client_id,
            "type" : type
        }
        
        json_data = None
        if old_models:
            json_data = [model.model_dump() for model in old_models]
            
        response = await client.post(f"http://{HOST}:8005/get_excel_data", 
                                     params=params,
                                     json=json_data,
                                     timeout=60)
        
        if response.status_code != 200:
            logging.error(response.text)
        
        return response.content
    
async def validate_excel_data(user_client_id: int, type: str, filepath: str):
    with open(filepath, 'rb') as filedata:
        async with httpx.AsyncClient() as client:
            params = {
                "user_client_id" : user_client_id,
                "type" : type
            }
            
            response = await client.post(f"http://{HOST}:8005/validate_excel_data", 
                                        params=params,
                                        files={"new_file_data" : (filepath, filedata)}, 
                                        timeout=60)
            
            if response.status_code != 200:
                logging.error(response.text)
            
            info = response.json()
            return info