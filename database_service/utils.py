import asyncio
import datetime
import logging
from typing import List

import asyncpg

from shared_files.models import (CClientReturn, CClientSpending,
                                 CDefectCompensation, CIncome, CItem,
                                 CLostItemCompensation, COrder, CPayment,
                                 CPenaltie, CRealPriceItem, CReturn, CStock,
                                 CStoragesInfo, CStornoLogic, CStornoSale)


async def health_check_connection():
    while True:
        try:
            await asyncpg.connect(**DB_CFG)
            logging.info(f"Connection to database is ok")
            break
        except Exception as e:
            logging.info(f"Connection refused during healthcheck: {e}")
            await asyncio.sleep(1)
            
async def select_data(table_name, columns, where_condition=None):
    conn = await asyncpg.connect(**DB_CFG)
    # Собираем SQL-запрос с использованием asyncpg
    select_query = f"SELECT {', '.join(columns)} FROM wb_data.{table_name}"

    if where_condition:
        select_query += f" WHERE {where_condition}"

    # Выполняем запрос SELECT
    result = await conn.fetch(select_query)
    await conn.close()
    return result

async def update_data(table_name, models, where_condition):
    conn = await asyncpg.connect(**DB_CFG)
    for model in models:
        set_vals = ""
        for arg_name, arg_value in vars(model).items():
            if arg_value != None:
                if type(arg_value) != str:
                    set_vals += f"{arg_name} = {arg_value}, "
                else:
                    set_vals += f"{arg_name} = '{arg_value}', "
        
        # Собираем SQL-запрос с использованием asyncpg
        update_query = f"UPDATE wb_data.{table_name} SET {set_vals[:-2]} WHERE {where_condition}"
        logging.info(update_query)
        # Выполняем запрос на обновление
        await conn.execute(update_query)

    # Фиксируем изменения
    await conn.close()

async def insert_data(table_name, columns, data_to_insert):
    conn = await asyncpg.connect(**DB_CFG)
    vals = ""
    for i in range(1, len(columns) + 1):
        vals += f"${i}, "
    
    # Собираем SQL-запрос с использованием asyncpg
    insert_query = f"INSERT INTO wb_data.{table_name} ({', '.join(columns)}) VALUES ({vals[:-2]})"
    # Выполняем множественную вставку
    await conn.executemany(insert_query, data_to_insert)

    # Фиксируем изменения
    await conn.close()

async def create_partitions(date):
    conn = await asyncpg.connect(**DB_CFG)
    select_query = f"SELECT create_date_partition('{date}')"
    result = await conn.fetch(select_query)

    return result

async def create_final_report(user_client_id: int, date_from, date_to):
    conn = await asyncpg.connect(**DB_CFG)
    select_query = f"SELECT * FROM create_final_report({user_client_id}, '{date_from}', '{date_to}')"
    resp = await conn.fetch(select_query)
    return resp

async def create_orders_agg_before_real_cost_update(user_client_id: int, date_from, date_to):
    if date_from == None or date_to == None:
        # Первая сессия
        conn = await asyncpg.connect(**DB_CFG)
        select_query = f"SELECT create_orders_agg_first_session_step_1({user_client_id})"
        result = await conn.fetch(select_query)
    else:
        # N-ая сессия
        conn = await asyncpg.connect(**DB_CFG)
        select_query = f"SELECT create_orders_agg_n_session_step_1({user_client_id}, '{date_from}', '{date_to}')"
        result = await conn.fetch(select_query)
        
    return result

async def create_orders_agg_after_real_cost_update(user_client_id: int, date_from, date_to):
    if date_from == None or date_to == None:
        # Первая сессия
        conn = await asyncpg.connect(**DB_CFG)
        select_query = f"SELECT create_orders_agg_first_session_step_2({user_client_id})"
        result = await conn.fetch(select_query)
    else:
        # N-ая сессия
        conn = await asyncpg.connect(**DB_CFG)
        select_query = f"SELECT create_orders_agg_n_session_step_2({user_client_id}, '{date_from}', '{date_to}')"
        result = await conn.fetch(select_query)
        
    return result

async def insert_orders(orders: List[COrder]):
    columns = [ "order_id", "user_client_id", "item_id", "income_id", 
                "order_dt", "shk_id", "delivery_price_rub", 
                "site_country", "size", "month"
              ]
    
    data_to_insert = [
        (
            order.order_id, order.user_client_id, order.item_id,
            order.income_id, datetime.datetime.strptime(order.order_dt, "%Y-%m-%d"), 
            order.shk_id, order.delivery_price_rub, order.site_country,
            order.size, datetime.datetime.strptime(order.month, "%Y-%m-%d")
        )
        for order in orders
    ]
    
    await insert_data('orders', columns, data_to_insert)
    
async def insert_payments(payments: List[CPayment]):
    columns = [ "order_id", "user_client_id", "item_id",
                "sale_dt", "retail_price_withdisc_rub", "commission_percent", 
                "commission_rub", "retail_price_without_com_rub", "month"
              ]
    
    data_to_insert = [
        (
            payment.order_id, payment.user_client_id, payment.item_id,
            datetime.datetime.strptime(payment.sale_dt, "%Y-%m-%d"), 
            payment.retail_price_withdisc_rub,
            payment.commission_percent, payment.commission_rub,
            payment.retail_price_without_com_rub, 
            datetime.datetime.strptime(payment.month, "%Y-%m-%d")
        )
        for payment in payments
    ]
    
    await insert_data('orders_payment', columns, data_to_insert)
    
async def insert_returns(returns: List[CReturn]):
    columns = [ "order_id", "user_client_id", "item_id",
                "return_dt", "return_price_rub", "month"
              ]
    
    data_to_insert = [
        (
            return_.order_id, return_.user_client_id, return_.item_id,
            datetime.datetime.strptime(return_.return_dt, "%Y-%m-%d"),
            return_.return_price_rub, 
            datetime.datetime.strptime(return_.month, "%Y-%m-%d")
        )
        for return_ in returns
    ]
    
    await insert_data('orders_returns', columns, data_to_insert)
    
async def insert_penalties(penalties: List[CPenaltie]):
    columns = [ "order_id", "user_client_id", "item_id",
                "client_penalty_dt", "penalty_price_rub", "penalty_type",
                "month"
              ]
    
    data_to_insert = [
        (
            penaltie.order_id, penaltie.user_client_id, penaltie.item_id,
            datetime.datetime.strptime(penaltie.client_penalty_dt, "%Y-%m-%d"),
            penaltie.penalty_price_rub, penaltie.penalty_type, 
            datetime.datetime.strptime(penaltie.month, "%Y-%m-%d")
        )
        for penaltie in penalties
    ]
    
    await insert_data('penalties', columns, data_to_insert)
    
async def insert_client_returns(client_returns: List[CClientReturn]):
    columns = [ "order_id", "user_client_id", "item_id",
                "client_return_dt", "return_price_rub", "month"
              ]
    
    data_to_insert = [
        (
            client_return.order_id, client_return.user_client_id, client_return.item_id,
            datetime.datetime.strptime(client_return.client_return_dt, "%Y-%m-%d"),
            client_return.return_price_rub, 
            datetime.datetime.strptime(client_return.month, "%Y-%m-%d")
        )
        for client_return in client_returns
    ]
    
    await insert_data('client_returns', columns, data_to_insert)
    
async def insert_stornos_sales(stornos_sales: List[CStornoSale]):
    columns = [ "order_id", "user_client_id", "item_id",
                "client_storno_dt", "storno_price_rub", "month"
              ]
    
    data_to_insert = [
        (
            stornos_sale.order_id, stornos_sale.user_client_id, stornos_sale.item_id,
            datetime.datetime.strptime(stornos_sale.client_storno_dt, "%Y-%m-%d"),
            stornos_sale.storno_price_rub, 
            datetime.datetime.strptime(stornos_sale.month, "%Y-%m-%d")
        )
        for stornos_sale in stornos_sales
    ]
    
    await insert_data('storno_sales', columns, data_to_insert)
    
async def insert_stornos_logic(stornos_logics: List[CStornoLogic]):
    columns = [ "order_id", "user_client_id", "item_id",
                "logistic_storno_dt", "storno_amount_rub", "month"
              ]
    
    data_to_insert = [
        (
            stornos_logic.order_id, stornos_logic.user_client_id, stornos_logic.item_id,
            datetime.datetime.strptime(stornos_logic.logistic_storno_dt, "%Y-%m-%d"),
            stornos_logic.storno_amount_rub, 
            datetime.datetime.strptime(stornos_logic.month, "%Y-%m-%d")
        )
        for stornos_logic in stornos_logics
    ]
    
    await insert_data('storno_logistic', columns, data_to_insert)
    
async def insert_lost_items_compensation(lost_item_compensations: List[CLostItemCompensation]):
    columns = [ "order_id", "user_client_id", "item_id",
                "lost_compensation_dt", "compensation_amount_rub", 
                "compensation_type", "month"
              ]
    
    data_to_insert = [
        (
            lost_item_compensation.order_id, lost_item_compensation.user_client_id, lost_item_compensation.item_id,
            datetime.datetime.strptime(lost_item_compensation.lost_compensation_dt, "%Y-%m-%d"),
            lost_item_compensation.compensation_amount_rub, lost_item_compensation.compensation_type, 
            datetime.datetime.strptime(lost_item_compensation.month, "%Y-%m-%d")
        )
        for lost_item_compensation in lost_item_compensations
    ]
    
    await insert_data('lost_item_compensation', columns, data_to_insert)
    
async def insert_defects_compensation(defect_compensations: List[CDefectCompensation]):
    columns = [ "order_id", "user_client_id", "item_id",
                "client_compensation_dt", "compensation_amount_rub", 
                "compensation_type", "month"
              ]
    
    data_to_insert = [
        (
            defect_compensation.order_id, defect_compensation.user_client_id, defect_compensation.item_id,
            datetime.datetime.strptime(defect_compensation.client_compensation_dt, "%Y-%m-%d"),
            defect_compensation.compensation_amount_rub, defect_compensation.compensation_type, 
            datetime.datetime.strptime(defect_compensation.month, "%Y-%m-%d")
        )
        for defect_compensation in defect_compensations
    ]
    
    await insert_data('defect_compensation', columns, data_to_insert)
    
    
async def insert_items(items: List[CItem]):
    columns = [ "item_id", "user_client_id", "current_price", 
               "vendor_code", "category", "subject", "brand"
              ]
    
    data_to_insert = [
        (
            item.item_id, item.user_client_id, item.current_price,
            item.vendor_code, item.category, item.subject,
            item.brand
        )
        for item in items
    ]
    
    await insert_data('items', columns, data_to_insert)
    
async def insert_incomes(incomes: List[CIncome]):
    columns = [ "item_id", "income_id", "user_client_id", 
               "income_dt", "quantity", "month"
              ]
    
    data_to_insert = [
        (
            income.item_id, income.income_id, income.user_client_id,
            datetime.datetime.strptime(income.income_dt, "%Y-%m-%d"),
            income.quantity, datetime.datetime.strptime(income.month, "%Y-%m-%d")
        )
        for income in incomes
    ]
    
    await insert_data('Items_incomes', columns, data_to_insert)
    
async def insert_stocks(stocks: List[CStock]):
    columns = [ "item_id", "storage_id", "user_client_id", 
               "quantity", "quantity_full", "month"
              ]
    
    data_to_insert = [
        (
            stock.item_id, stock.storage_id, stock.user_client_id,
            stock.quantity, stock.quantity_full, 
            datetime.datetime.strptime(stock.month, "%Y-%m-%d")
        )
        for stock in stocks
    ]
    
    await insert_data('Items_storages', columns, data_to_insert)
    
async def insert_client_spendings(client_spendings: List[CClientSpending]):
    columns = [ "user_client_id", "spending_name", "price", 
               "frequency", "start_dt", "end_dt"
              ]
    
    end_dt = None
    data_to_insert = [
        (
            client_spending.user_client_id, client_spending.spending_name, client_spending.price,
            client_spending.frequency,
            datetime.datetime.strptime(client_spending.start_dt, "%Y-%m-%d"),
            datetime.datetime.strptime(client_spending.end_dt, "%Y-%m-%d") if client_spending.end_dt else end_dt
        )
        for client_spending in client_spendings
    ]
    
    await insert_data('Clients_spendings', columns, data_to_insert)
    
async def insert_real_price_items(real_price_items: List[CRealPriceItem]):
    columns = [ "item_id", "user_client_id", 
               "item_real_price", "start_dt"
              ]
    
    data_to_insert = [
        (
            real_price_item.item_id, real_price_item.user_client_id, real_price_item.item_real_price,
            datetime.datetime.strptime(real_price_item.start_dt, "%Y-%m-%d")
        )
        for real_price_item in real_price_items
    ]
    
    await insert_data('item_real_price_history', columns, data_to_insert)
    
async def insert_storages_infos(storages_infos: List[CStoragesInfo]):
    columns = [ "unit_name", "storage_name", "logic_price_per_five_liter", 
               "logic_additional_price_per_liter", "hold_price_per_one_pallet",
               "hold_price_per_five_liter", "hold_additional_price_per_liter",
               "active_flg"
              ]
    
    data_to_insert = [
        (
            storages_info.unit_name, storages_info.storage_name, 
            storages_info.logic_price_per_five_liter, storages_info.logic_additional_price_per_liter,
            storages_info.hold_price_per_one_pallet, storages_info.hold_price_per_five_liter,
            storages_info.hold_additional_price_per_liter, storages_info.active_flg
        )
        for storages_info in storages_infos
    ]
    
    await insert_data('storages_info', columns, data_to_insert)
    
async def insert_client(tg_id, tg_username, first_name, last_name, is_subcriber, mobile_phone=""):
    columns = ["mobile_phone", "tg_id", "tg_username", "first_name", "last_name", "is_subcriber"]
    
    data_to_insert = [
        (
            mobile_phone, tg_id, tg_username, first_name, last_name, is_subcriber
        )
    ]
    
    await insert_data('clients', columns, data_to_insert)
    
async def select_storages_infos(condition: str):
    columns = ["id", "unit_name", "storage_name", "logic_price_per_five_liter", 
               "logic_additional_price_per_liter", "hold_price_per_one_pallet",
               "hold_price_per_five_liter", "hold_additional_price_per_liter", "active_flg", "load_time"]
    
    return await select_data('Storages_info', columns, condition)
    
async def select_other_spendings(condition: str):
    columns = ["spending_id", "spending_name",
               "price", "frequency", "start_dt",
               "end_dt", "user_client_id"]
    
    return await select_data('Clients_spendings', columns, condition)
    
async def select_real_price_items(condition: str):
    columns = ["item_id", "item_real_price",
               "start_dt", "user_client_id"]
    
    return await select_data('item_real_price_history', columns, condition)
    
async def select_items(condition: str):
    columns = ["item_id", "user_client_id", "current_price",
               "vendor_code", "category", "subject",
               "brand", "last_event_dt"]
    
    return await select_data('Items', columns, condition)

async def select_clients(condition: str):
    columns = ["user_client_id", "tg_id",
               "tg_username", "is_subcriber", "wb_token"]
    
    return await select_data('Clients', columns, condition)