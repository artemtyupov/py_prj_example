import datetime
import uuid

from shared_files.models import (CClientReturn, CDefectCompensation,
                                 CLostItemCompensation, COrder, CPayment,
                                 CPenaltie, CReturn, CStornoLogic, CStornoSale)


def get_data_from_detail_reports(detail_reports, user_client_id):
    orders = {}
    payments = {}
    returns = {}
    penalties = {}
    defects_compensation = {}
    lost_items_compensation = {}
    stornos_sales = {}
    stornos_logic = {}
    client_returns = {}
    for detail_report in detail_reports:
        doc_type = detail_report["doc_type_name"]
        supplier_oper_name = detail_report["supplier_oper_name"]
        item_id = detail_report['nm_id']
        if doc_type == "Продажа" and supplier_oper_name == "Логистика" and detail_report["delivery_amount"] > 0:
            order_dt = datetime.datetime.strptime(detail_report["rr_dt"], '%Y-%m-%dT%H:%M:%SZ').date()
            orders[detail_report['srid']] = COrder(order_id=str(uuid.uuid4()),
                                                   user_client_id=user_client_id,
                                                   item_id=item_id,
                                                   income_id=detail_report['gi_id'],
                                                   order_dt=order_dt.strftime('%Y-%m-%d'),
                                                   shk_id=detail_report['shk_id'],
                                                   delivery_price_rub=detail_report['delivery_rub'],
                                                   site_country=detail_report['site_country'],
                                                   size=detail_report['ts_name'],
                                                   month=order_dt.strftime('%Y-%m-01'))
            
        elif doc_type == "Продажа" and supplier_oper_name == "Логистика" and detail_report["return_amount"] > 0:
            rr_dt = datetime.datetime.strptime(detail_report["rr_dt"], '%Y-%m-%dT%H:%M:%SZ').date()
            returns[detail_report['srid']] = CReturn(order_id="",
                                                     item_id=item_id,
                                                     user_client_id=user_client_id,
                                                     return_dt=rr_dt.strftime('%Y-%m-%d'),
                                                     return_price_rub=detail_report['delivery_rub'],
                                                     month=rr_dt.strftime('%Y-%m-01'))
            
        elif doc_type == "Продажа" and supplier_oper_name in ["Продажа",  "Корректная продажа"]:
            retail_price_withdisc_rub = detail_report["retail_price_withdisc_rub"]
            commission_percent = detail_report["commission_percent"]
            commission_rub = retail_price_withdisc_rub * commission_percent
            retail_price_without_com_rub = retail_price_withdisc_rub - commission_rub
            sale_dt = datetime.datetime.strptime(detail_report["rr_dt"], '%Y-%m-%dT%H:%M:%SZ').date()
            payments[detail_report['srid']] = CPayment(order_id="",
                                                       user_client_id=user_client_id,
                                                       item_id=item_id,
                                                       sale_dt=sale_dt.strftime('%Y-%m-%d'),
                                                       retail_price_withdisc_rub=retail_price_withdisc_rub,
                                                       commission_percent=commission_percent,
                                                       commission_rub=commission_rub,
                                                       retail_price_without_com_rub=retail_price_without_com_rub,
                                                       month=sale_dt.strftime('%Y-%m-01'))
            
        elif doc_type == "Продажа" and supplier_oper_name in ["Штрафы"]:
            client_penalty_dt = datetime.datetime.strptime(detail_report["rr_dt"], '%Y-%m-%dT%H:%M:%SZ').date()
            penalty_price_rub = detail_report["penalty"]
            penalty_type = detail_report["bonus_type_name"] if "bonus_type_name" in detail_report else "Не указано"
            penalties[detail_report['srid']] = CPenaltie(order_id="",
                                                         item_id=item_id,
                                                         user_client_id=user_client_id,
                                                         client_penalty_dt=client_penalty_dt.strftime('%Y-%m-%d'),
                                                         penalty_price_rub=penalty_price_rub,
                                                         penalty_type=penalty_type,
                                                         month=client_penalty_dt.strftime('%Y-%m-01'))
                                                         
        elif doc_type in ["Продажа", "Возврат"] and supplier_oper_name in  ["Частичная компенсация брака", "Оплата брака"]:
            client_compensation_dt = datetime.datetime.strptime(detail_report["rr_dt"], '%Y-%m-%dT%H:%M:%SZ').date()
            compensation_amount_rub = detail_report["retail_price_withdisc_rub"]
            compensation_type = detail_report["bonus_type_name"] if "bonus_type_name" in detail_report else "Не указано"
            defects_compensation[detail_report['srid']] = CDefectCompensation(order_id="",
                                                                              item_id=item_id,
                                                                              user_client_id=user_client_id,
                                                                              client_compensation_dt=client_compensation_dt.strftime('%Y-%m-%d'),
                                                                              compensation_amount_rub=compensation_amount_rub,
                                                                              compensation_type=compensation_type,
                                                                              month=client_compensation_dt.strftime('%Y-%m-01'))
            
        elif doc_type in ["Продажа", "Возврат"] and supplier_oper_name in ["Авансовая оплата за товар без движения", "Оплата потерянного товара"]:
            lost_compensation_dt = datetime.datetime.strptime(detail_report["rr_dt"], '%Y-%m-%dT%H:%M:%SZ').date()
            compensation_amount_rub = detail_report["retail_price_withdisc_rub"]
            compensation_type = detail_report["bonus_type_name"] if "bonus_type_name" in detail_report else "Не указано"
            lost_items_compensation[detail_report['srid']] = CLostItemCompensation(order_id="",
                                                                                   item_id=item_id,
                                                                                   user_client_id=user_client_id,
                                                                                   lost_compensation_dt=lost_compensation_dt.strftime('%Y-%m-%d'),
                                                                                   compensation_amount_rub=compensation_amount_rub,
                                                                                   compensation_type=compensation_type,
                                                                                   month=lost_compensation_dt.strftime('%Y-%m-01'))
        elif doc_type == "Продажа"and supplier_oper_name == "Логистика сторно":
            logistic_storno_dt = datetime.datetime.strptime(detail_report["rr_dt"], '%Y-%m-%dT%H:%M:%SZ').date()
            storno_amount_rub = detail_report["delivery_rub"]
            stornos_logic[detail_report['srid']] = CStornoLogic(order_id="",
                                                                item_id=item_id,
                                                                user_client_id=user_client_id,
                                                                logistic_storno_dt=logistic_storno_dt.strftime('%Y-%m-%d'),
                                                                storno_amount_rub=storno_amount_rub,
                                                                month=logistic_storno_dt.strftime('%Y-%m-01'))
            
        elif doc_type == "Возврат" and supplier_oper_name == "Сторно продаж":
            client_storno_dt = datetime.datetime.strptime(detail_report["rr_dt"], '%Y-%m-%dT%H:%M:%SZ').date()
            storno_price_rub = detail_report["retail_price_withdisc_rub"]
            stornos_sales[detail_report['srid']] = CStornoSale(order_id="",
                                                               item_id=item_id,
                                                               user_client_id=user_client_id,
                                                               client_storno_dt=client_storno_dt.strftime('%Y-%m-%d'),
                                                               storno_price_rub=storno_price_rub,
                                                               month=client_storno_dt.strftime('%Y-%m-01'))
            
        elif doc_type == "Возврат" and supplier_oper_name == "Возврат":
            client_return_dt = datetime.datetime.strptime(detail_report["rr_dt"], '%Y-%m-%dT%H:%M:%SZ').date()
            return_price_rub = detail_report["retail_price_withdisc_rub"]
            client_returns[detail_report['srid']] = CClientReturn(order_id="",
                                                                  item_id=item_id,
                                                                  user_client_id=user_client_id,
                                                                  client_return_dt=client_return_dt.strftime('%Y-%m-%d'),
                                                                  return_price_rub=return_price_rub,
                                                                  month=client_return_dt.strftime('%Y-%m-01'))
        else:
            stop = 0
        
    def fill_order_id(container):
        for srid, val in container.items():
            if srid not in orders:
                val.order_id = str(uuid.uuid4())
                continue
            
            val.order_id = orders[srid].order_id
            
    fill_order_id(payments)
    fill_order_id(returns)
    fill_order_id(defects_compensation)
    fill_order_id(lost_items_compensation)
    fill_order_id(stornos_sales)
    fill_order_id(stornos_logic)
    fill_order_id(client_returns)
    fill_order_id(penalties)
    
    return list(orders.values()), list(payments.values()), list(returns.values()),\
           list(defects_compensation.values()), list(lost_items_compensation.values()),\
           list(stornos_sales.values()), list(stornos_logic.values()),\
           list(client_returns.values()), list(penalties.values())
