# server.py

import logging
import sys

from fastapi import FastAPI, HTTPException, status

sys.path.append(".")
sys.path.append("..")

from typing import List

from utils import (create_orders_agg_after_real_cost_update,
                   create_orders_agg_before_real_cost_update,
                   create_partitions, health_check_connection, insert_client,
                   insert_client_returns, insert_client_spendings,
                   insert_defects_compensation, insert_incomes, insert_items,
                   insert_lost_items_compensation, insert_orders,
                   insert_payments, insert_penalties, insert_real_price_items,
                   insert_returns, insert_stocks, insert_storages_infos,
                   insert_stornos_logic, insert_stornos_sales, select_clients,
                   select_items, select_other_spendings, create_final_report,
                   select_real_price_items, select_storages_infos, update_data)

from shared_files.models import (CClient, CClientReturn, CClientSpending,
                                 CDefectCompensation, CIncome, CItem,
                                 CLostItemCompensation, COrder, CPayment,
                                 CPenaltie, CRealPriceItem, CReturn, CStock,
                                 CStoragesInfo, CStornoLogic, CStornoSale)

app = FastAPI()

# Настройка логирования
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO)

@app.get("/health")#, methods=["GET", "POST", "PUT"])
async def helthcheck():
    await health_check_connection()
    return status.HTTP_204_NO_CONTENT

@app.post("/insert/orders")
async def process(orders: List[COrder]):
    try:
        await insert_orders(orders)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/payments")
async def process(payments: List[CPayment]):
    try:
        await insert_payments(payments)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/insert/returns")
async def process(returns: List[CReturn]):
    try:
        await insert_returns(returns)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/penalties")
async def process(penalties: List[CPenaltie]):
    try:
        await insert_penalties(penalties)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/client_returns")
async def process(client_returns: List[CClientReturn]):
    try:
        await insert_client_returns(client_returns)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/stornos_sales")
async def process(sales: List[CStornoSale]):
    try:
        await insert_stornos_sales(sales)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/stornos_logic")
async def process(logics: List[CStornoLogic]):
    try:
        await insert_stornos_logic(logics)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/lost_items_compensation")
async def process(lost_items: List[CLostItemCompensation]):
    try:
        await insert_lost_items_compensation(lost_items)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/defects_compensation")
async def process(defects: List[CDefectCompensation]):
    try:
        await insert_defects_compensation(defects)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/items")
async def process(items: List[CItem]):
    try:
        await insert_items(items)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/incomes")
async def process(incomes: List[CIncome]):
    try:
        await insert_incomes(incomes)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/stocks")
async def process(stocks: List[CStock]):
    try:
        await insert_stocks(stocks)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/client_spendings")
async def process(client_spendings: List[CClientSpending]):
    try:
        await insert_client_spendings(client_spendings)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/real_price_items")
async def process(real_price_items: List[CRealPriceItem]):
    try:
        await insert_real_price_items(real_price_items)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/storages_infos")
async def process(storages_infos: List[CStoragesInfo]):
    try:
        await insert_storages_infos(storages_infos)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/insert/client")
async def process(client: CClient):
    try:
        await insert_client(client.tg_id, 
                            client.tg_username, 
                            client.first_name,
                            client.last_name,
                            client.is_subcriber,
                            client.mobile_phone)
        
        return status.HTTP_204_NO_CONTENT
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/select/other_spendings")
async def process(condition: str = None):
    try:
        return await select_other_spendings(condition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/select/real_price_items")
async def process(condition: str = None):
    try:
        return await select_real_price_items(condition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/select/clients")
async def process(condition: str = None):
    try:
        return await select_clients(condition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/select/items")
async def process(condition: str = None):
    try:
        return await select_items(condition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/select/storages_infos")
async def process(condition: str = None):
    try:
        return await select_storages_infos(condition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/update/clients")
async def process(clients: List[CClient], condition: str = None):
    try:
        return await update_data('Clients', clients, condition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/update/client_spendings")
async def process(client_spendings: List[CClientSpending], condition: str = None):
    try:
        return await update_data('Clients_spendings', client_spendings, condition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/update/storages_infos")
async def process(storages_infos: List[CStoragesInfo], condition: str = None):
    try:
        return await update_data('Storages_info', storages_infos, condition)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/create/partitions")
async def process(date: str):
    try:
        return await create_partitions(date)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/create/orders_agg/before")
async def process(user_client_id: int, date_from: str = None, date_to: str = None):
    try:
        return await create_orders_agg_before_real_cost_update(user_client_id, date_from, date_to)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/create/orders_agg/after")
async def process(user_client_id: int, date_from: str = None, date_to: str = None):
    try:
        return await create_orders_agg_after_real_cost_update(user_client_id, date_from, date_to)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/get/final_report_data")
async def process(user_client_id: int, date_from: str = None, date_to: str = None):
    try:
        return await create_final_report(user_client_id, date_from, date_to)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)