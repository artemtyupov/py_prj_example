import datetime

import httpx


async def get_report(token: str, dateFrom: str, check: bool):
    headers = {"Authorization" : token}
    cur_date = datetime.datetime.now().date().strftime(f"%Y-%m-%d")
    limit = 100000 if not check else 10
    params = {"dateFrom" : dateFrom, "limit" : limit, "dateTo" : cur_date}
    rrd_id = 0
    result_api_response = []
    errs_cnt = 0
    # curl -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6ImZiM2Q0NDNjLWU1ZGQtNDkzNS05YzNmLWY4NWRhNWI2NTVmNCJ9.-TAHFF2rqaSolla-hVbgablqYJMg1zZGAI8Nnc4Mfbo" https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod
    async with httpx.AsyncClient() as client:
        while True:
            params["rrdid"] = rrd_id
            response = await client.get("https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod", params=params, headers=headers, timeout=60)
            if response.status_code != 200:
                if errs_cnt >= 50:
                    return []
                
                errs_cnt += 1
                continue
            json_data = response.json()
            if json_data == None:
                break
            
            if len(json_data) == 0:
                break
            else:
                result_api_response.extend(json_data)
                rrd_id = json_data[len(json_data) - 1]["rrd_id"]
                if len(json_data) < 100000:
                    break
                
                if check:
                    break
    
        return result_api_response

async def get_incomes(token: str, dateFrom: str):
    headers = {"Authorization" : token}
    params = {"dateFrom" : dateFrom}
    errs_cnt = 0
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get("https://statistics-api.wildberries.ru/api/v1/supplier/incomes", params=params, headers=headers, timeout=60)
            if response.status_code != 200:
                if errs_cnt >= 50:
                    return []
                
                errs_cnt += 1
                continue
            
            json_data = response.json()
            return json_data
    
async def get_stocks(token: str, dateFrom: str):
    headers = {"Authorization" : token}
    params = {"dateFrom" : dateFrom}
    errs_cnt = 0
    async with httpx.AsyncClient() as client:
        while True:
            response = await client.get("https://statistics-api.wildberries.ru/api/v1/supplier/stocks", params=params, headers=headers, timeout=60)
            if response.status_code != 200:
                if errs_cnt >= 50:
                    return []
                
                errs_cnt += 1
                continue
            
            json_data = response.json()
            return json_data