import datetime

import shared_files.database_works as db
from shared_files.api_works import get_incomes, get_report, get_stocks
from shared_files.construct_objects import get_data_from_detail_reports
from shared_files.models import CClient, CIncome, CItem


async def update_data_for_client(client: CClient):
    # выгружаем новые данные из АПИ
    cur_date = datetime.datetime.now().date()
    dateFrom = cur_date - datetime.timedelta(days=7)
    detail_reports = await get_report(client.wb_token, dateFrom, False)
    
    # распределение остальных данных
    orders, payments, returns, defects_compensation,\
    lost_items_compensation, stornos_sales,\
    stornos_logic, client_returns, penalties = get_data_from_detail_reports(detail_reports, client.user_client_id)
    
    # загружаем данные в бд
    await db.insert_orders(orders)
    await db.insert_payments(payments)
    await db.insert_returns(returns)
    await db.insert_defects_compensation(defects_compensation)
    await db.insert_lost_items_compensation(lost_items_compensation)
    await db.insert_stornos_sales(stornos_sales)
    await db.insert_stornos_logic(stornos_logic)
    await db.insert_client_returns(client_returns)
    await db.insert_penalties(penalties)
    
async def update_items_for_client(client: CClient):
    # выгружаем новые данные из АПИ
    cur_date = datetime.datetime.now().date()
    dateFrom = cur_date - datetime.timedelta(days=1)
    income_reports = await get_incomes(client.wb_token, dateFrom)
    stocks_reports = await get_stocks(client.wb_token, dateFrom)
    
    # TODO проверить корнер кейсы (хочу заполнять поставки из такого же критерия)
    # из income_reports берем уникальные строчки по nm_id (из одинаковых nm_id берем тот, который ближе к сегодняшней дате, то есть последний)
    unique_incomes_dict = {}
    for income_report in income_reports:
        nm_id = income_report['nmId']
        if nm_id not in unique_incomes_dict:
            unique_incomes_dict[nm_id] = income_report
        else:
            cur_date = datetime.datetime.strptime(unique_incomes_dict[nm_id]["date"], '%Y-%m-%dT%H:%M:%SZ').date()
            new_date = datetime.datetime.strptime(income_report["date"], '%Y-%m-%dT%H:%M:%SZ').date()
            if new_date > cur_date:
                unique_incomes_dict[nm_id] = income_report
            
    stocks_dict = {}
    for stock_report in stocks_reports:
        stocks_dict[stock_report['nmId']] = stock_report
        
        
    # сопоставляем уникальные unique_incomes_dict с stocks_dict по nm_id(если у поставки есть nm_id, которого нет на складе, то формируем [income_reports_not_in_stocks])
    income_reports_not_in_stocks = []
    for nm_id, income_report in unique_incomes_dict.items():
        if nm_id not in stocks_dict:
            income_reports_not_in_stocks.append(income_report)
        else:
            stocks_dict[nm_id]['gi_id'] = income_report['incomeId']
            
    # объединям income_reports_not_in_stocks и stocks_dict для формирования Items (все итемы со склада + итемы из поставок, которые распродались и их нет на складе)
    items_dict = {}
    for income in income_reports_not_in_stocks:
        # TODO Витя должен проверить нужно ли это
        """ item_price = income['totalPrice']
        if item_price == None:
            item_price = 0 """
            
        items_dict[income['nmId']] = CItem(item_id=income['nmId'],
                                            user_client_id=client.user_client_id,
                                            current_price=0,
                                            vendor_code=income['supplierArticle'],
                                            category='',
                                            subject='',
                                            brand='',
                                            gi_id=income['incomeId'])
        
        
    for nm_id, stock in stocks_dict.items():
        incomeId = 0
        if 'gi_id' in stock:
            incomeId = stock['gi_id']
        
        items_dict[nm_id] = CItem(item_id=nm_id,
                                  user_client_id=client.user_client_id,
                                  current_price=stock['Price'],
                                  vendor_code=stock['supplierArticle'],
                                  category=stock['category'],
                                  subject=stock['subject'],
                                  brand=stock['brand'],
                                  gi_id=incomeId)
        
    income_models = []
    for income_report in income_reports:
        income_dt = datetime.datetime.strptime(income_report['date'], '%Y-%m-%dT%H:%M:%S').date()
        income_models.append(CIncome(item_id=income_report['nmId'],
                                     income_id=income_report['incomeId'],
                                     user_client_id=client.user_client_id,
                                     income_dt=income_dt,
                                     quantity=income_report['quantity'],
                                     month=income_dt.strftime('%Y-%m-01')))
        
    stock_models = []
    for stock_report in stocks_reports:
        stock_models.append(CStock(item_id=nm_id,
                                   storage_id=storage_id,
                                   user_client_id=user_client_id,
                                   quantity=stock['quantity'],
                                   quantity_full=stock['quantityFull'],
                                   month=datetime.datetime.now().date().strftime('%Y-%m-01')))
        
    # вставка в бд
    await db.insert_items(list(items_dict.values()))
    await db.insert_incomes(income_models)