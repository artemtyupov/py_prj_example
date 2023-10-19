import asyncio
import logging
import os
from typing import List

import httpx

from shared_files.models import (CClient, CClientReturn, CClientSpending,
                                 CDefectCompensation, CIncome, CItem,
                                 CLostItemCompensation, COrder, CPayment,
                                 CPenaltie, CRealPriceItem, CReturn, CStock,
                                 CStoragesInfo, CStornoLogic, CStornoSale)

if os.getenv('IS_DOCKER') == "1":
    HOST = "database_service_container"
else:
    HOST = "localhost"

async def create_orders_agg_before_real_cost_update(user_client_id: int, date_from: str = None, date_to: str = None):
    async with httpx.AsyncClient() as client:
        params = {"user_client_id" : user_client_id}
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/create/orders_agg/before", params=params, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def create_orders_agg_after_real_cost_update(user_client_id: int, date_from: str = None, date_to: str = None):
    async with httpx.AsyncClient() as client:
        params = {"user_client_id" : user_client_id}
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/create/orders_agg/after", params=params, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def get_final_report_data(user_client_id: int, date_from: str = None, date_to: str = None):
    async with httpx.AsyncClient() as client:
        params = {"user_client_id" : user_client_id,
                  "date_from" : date_from,
                  "date_to" : date_to}
        
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.get(f"http://{HOST}:8002/get/final_report_data", params=params, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
        return response.json()

async def insert_orders(orders: List[COrder]):
    async with httpx.AsyncClient() as client:
        data = [order.model_dump() for order in orders]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/orders", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_payments(payments: List[CPayment]):
    async with httpx.AsyncClient() as client:
        data = [payment.model_dump() for payment in payments]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/payments", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_returns(returns: List[CReturn]):
    async with httpx.AsyncClient() as client:
        data = [return_.model_dump() for return_ in returns]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/returns", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_penalties(penalties: List[CPenaltie]):
    async with httpx.AsyncClient() as client:
        data = [penaltie.model_dump() for penaltie in penalties]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/penalties", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_client_returns(client_returns: List[CClientReturn]):
    async with httpx.AsyncClient() as client:
        data = [client_return.model_dump() for client_return in client_returns]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/client_returns", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_stornos_sales(stornos_sales: List[CStornoSale]):
    async with httpx.AsyncClient() as client:
        data = [stornos_sale.model_dump() for stornos_sale in stornos_sales]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/stornos_sales", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_stornos_logic(stornos_logics: List[CStornoLogic]):
    async with httpx.AsyncClient() as client:
        data = [stornos_logic.model_dump() for stornos_logic in stornos_logics]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/stornos_logic", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_lost_items_compensation(lost_items_compensations: List[CLostItemCompensation]):
    async with httpx.AsyncClient() as client:
        data = [lost_items_compensation.model_dump() for lost_items_compensation in lost_items_compensations]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/lost_items_compensation", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_defects_compensation(defects_compensations: List[CDefectCompensation]):
    async with httpx.AsyncClient() as client:
        data = [defects_compensation.model_dump() for defects_compensation in defects_compensations]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/defects_compensation", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_items(items: List[CItem]):
    async with httpx.AsyncClient() as client:
        data = [item.model_dump() for item in items]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/items", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_incomes(incomes: List[CIncome]):
    async with httpx.AsyncClient() as client:
        data = [income.model_dump() for income in incomes]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/incomes", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_stocks(stocks: List[CStock]):
    async with httpx.AsyncClient() as client:
        data = [stock.model_dump() for stock in stocks]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/stocks", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_client_spendings(client_spendings: List[CClientSpending]):
    async with httpx.AsyncClient() as client:
        data = [client_spending.model_dump() for client_spending in client_spendings]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/client_spendings", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_real_price_items(real_price_items: List[CRealPriceItem]):
    async with httpx.AsyncClient() as client:
        data = [real_price_item.model_dump() for real_price_item in real_price_items]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/real_price_items", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_storages_infos(storages_infos: List[CStoragesInfo]):
    async with httpx.AsyncClient() as client:
        data = [storages_info.model_dump() for storages_info in storages_infos]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/storages_infos", json=data, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
            
async def insert_client(client_: CClient):
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/insert/client", json=client_.model_dump(), headers=headers)
        if response.status_code != 200:
            logging.error(response.text)
    
async def wait_for_database_service_ready():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://{HOST}:8002/health", timeout=250)
                response.raise_for_status()
                break
        
        except Exception as e:
            logging.info(f"Waiting for database service: {e}")
            await asyncio.sleep(1)
    
async def create_partitions(date: str):
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.post(f"http://{HOST}:8002/create/partitions", params={"date": date}, headers=headers)
        if response.status_code != 200:
            logging.error(response.text)

async def select_clients(condition: str = None):
    async with httpx.AsyncClient() as client:
        params = {}
        if condition:
            params = {"condition" : condition}
            
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.get(f"http://{HOST}:8002/select/clients", headers=headers, params=params)
        if response.status_code != 200:
            logging.error(response.text)

        clients = response.json()
        
        if len(clients) == 0:
            return []
        
        clients_models = []
        for cl in clients:
            client_ = CClient.model_validate(cl)
            clients_models.append(client_)
        
        return clients_models

async def select_items(condition: str = None) -> List[CItem]:
    async with httpx.AsyncClient() as client:
        params = {}
        if condition:
            params = {"condition" : condition}
            
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.get(f"http://{HOST}:8002/select/items", headers=headers, params=params)
        if response.status_code != 200:
            logging.error(response.text)
            
        items = response.json()
        items_models = []
        for item in items:
            items_models.append(CItem.model_validate(item))
            
        return items_models
    
async def select_storages_infos(condition: str = None) -> List[CStoragesInfo]:
    async with httpx.AsyncClient() as client:
        params = {}
        if condition:
            params = {"condition" : condition}
            
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.get(f"http://{HOST}:8002/select/storages_infos", headers=headers, params=params)
        if response.status_code != 200:
            logging.error(response.text)
            
        storages_infos = response.json()
        storages_infos_models = []
        for storages_info in storages_infos:
            storages_infos_models.append(CStoragesInfo.model_validate(storages_info))
            
        return storages_infos_models
            
    
async def select_other_spendings(condition: str = None) -> List[CClientSpending]:
    async with httpx.AsyncClient() as client:
        params = {}
        if condition:
            params = {"condition" : condition}
            
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.get(f"http://{HOST}:8002/select/other_spendings", headers=headers, params=params)
        if response.status_code != 200:
            logging.error(response.text)
            
        spendings = response.json()
        spending_models = []
        for spending in spendings:
            spending['status'] = CClientSpending.Status.DEFAULT.value
            spending_models.append(CClientSpending.model_validate(spending))
            
        return spending_models
    
async def select_real_price_items(condition: str = None) -> List[CRealPriceItem]:
    async with httpx.AsyncClient() as client:
        params = {}
        if condition:
            params = {"condition" : condition}
            
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        response = await client.get(f"http://{HOST}:8002/select/real_price_items", headers=headers, params=params)
        if response.status_code != 200:
            logging.error(response.text)
            
        real_price_items = response.json()
        real_price_items_models = []
        for real_price_item in real_price_items:
            real_price_items.append(CClientSpending.model_validate(real_price_item))
            
        return real_price_items_models
   
async def update_clients(clients: List[CClient], condition: str = None):
    async with httpx.AsyncClient() as client:
        data = [client_.model_dump() for client_ in clients]
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        params = {}
        if condition:
            params = {"condition" : condition}
            
        response = await client.post(f"http://{HOST}:8002/update/clients", json=data, headers=headers, params=params)
        if response.status_code != 200:
            logging.error(response.text)
            
        return response.json()

async def update_client_spendings(client_spendings: List[CClientSpending], condition: str = None):
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        params = {}
        if condition:
            params = {"condition" : condition}
        
        data = [client_spending.model_dump() for client_spending in client_spendings]
        
        response = await client.post(f"http://{HOST}:8002/update/client_spending", json=data, headers=headers, params=params)
        if response.status_code != 200:
            logging.error(response.text)
            
        return response.json()
    
async def update_storages_infos(update_storages_infos: List[CStoragesInfo], condition: str = None):
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json", "accept" : "application/json"}
        params = {}
        if condition:
            params = {"condition" : condition}
        
        data = [update_storages_info.model_dump() for update_storages_info in update_storages_infos]
        
        response = await client.post(f"http://{HOST}:8002/update/storages_infos", json=data, headers=headers, params=params)
        if response.status_code != 200:
            logging.error(response.text)
            
        return response.json()
