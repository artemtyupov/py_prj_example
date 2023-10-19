from typing import List, Optional

from aenum import AutoNumberEnum
from pydantic import BaseModel


class COrder(BaseModel):
    order_id: Optional[str] = None
    user_client_id: Optional[int] = None
    item_id: Optional[int] = None
    income_id: Optional[int] = None
    order_dt: Optional[str] = None
    shk_id: Optional[int] = None
    delivery_price_rub: Optional[float] = None
    site_country: Optional[str] = None
    size: Optional[str] = None
    month: Optional[str] = None

class CClient(BaseModel):
    user_client_id: Optional[int] = None
    mobile_phone: Optional[str] = None
    tg_id: Optional[int] = None
    tg_username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_subcriber: Optional[bool] = None
    wb_token: Optional[str] = None
    subscribe_end_dt: Optional[str] = None
    
class CPayment(BaseModel):
    order_id: Optional[str] = None
    user_client_id: Optional[int] = None
    item_id: Optional[int] = None
    sale_dt: Optional[str] = None
    retail_price_withdisc_rub: Optional[float] = None
    commission_percent: Optional[float] = None
    commission_rub: Optional[float] = None
    retail_price_without_com_rub: Optional[float] = None
    month: Optional[str] = None

class CReturn(BaseModel):
    order_id: Optional[str] = None
    item_id: Optional[int] = None
    user_client_id: Optional[int] = None
    return_dt: Optional[str] = None
    return_price_rub: Optional[float] = None
    month: Optional[str] = None

class CItem(BaseModel):
    item_id: Optional[int] = None
    user_client_id: Optional[int] = None
    current_price: Optional[float] = None
    vendor_code: Optional[str] = None
    category: Optional[str] = None
    subject: Optional[str] = None
    brand: Optional[str] = None
    last_event_dt: Optional[str] = None
    update_time: Optional[str] = None
    
    # не для бд
    gi_id: Optional[int] = None

class CItemRealPriceHistory(BaseModel):
    item_id: Optional[int] = None
    user_client_id: Optional[int] = None
    item_real_price: Optional[float] = None
    month: Optional[str] = None

class CIncome(BaseModel):
    item_id: Optional[int] = None
    income_id: Optional[int] = None
    user_client_id: Optional[int] = None
    income_dt: Optional[str] = None
    quantity: Optional[int] = None
    month: Optional[str] = None

class CStock(BaseModel):
    item_id: Optional[int] = None
    storage_id: Optional[int] = None
    user_client_id: Optional[int] = None
    quantity: Optional[int] = None
    quantity_full: Optional[int] = None
    month: Optional[str] = None

class CPenaltie(BaseModel):
    order_id: Optional[str] = None
    user_client_id: Optional[int] = None
    item_id: Optional[int] = None
    client_penalty_dt: Optional[str] = None
    penalty_price_rub: Optional[float] = None
    penalty_type: Optional[str] = None
    month: Optional[str] = None

class CDefectCompensation(BaseModel):
    order_id: Optional[str] = None
    user_client_id: Optional[int] = None
    item_id: Optional[int] = None
    client_compensation_dt: Optional[str] = None
    compensation_amount_rub: Optional[float] = None
    compensation_type: Optional[str] = None
    month: Optional[str] = None

class CLostItemCompensation(BaseModel):
    order_id: Optional[str] = None
    user_client_id: Optional[int] = None
    item_id: Optional[int] = None
    lost_compensation_dt: Optional[str] = None
    compensation_amount_rub: Optional[float] = None
    compensation_type: Optional[str] = None
    month: Optional[str] = None

class CStornoLogic(BaseModel):
    order_id: Optional[str] = None
    user_client_id: Optional[int] = None
    item_id: Optional[int] = None
    logistic_storno_dt: Optional[str] = None
    storno_amount_rub: Optional[float] = None
    month: Optional[str] = None

class CStornoSale(BaseModel):
    order_id: Optional[str] = None
    user_client_id: Optional[int] = None
    item_id: Optional[int] = None
    client_storno_dt: Optional[str] = None
    storno_price_rub: Optional[float] = None
    month: Optional[str] = None

class CClientReturn(BaseModel):
    order_id: Optional[str] = None
    user_client_id: Optional[int] = None
    item_id: Optional[int] = None
    client_return_dt: Optional[str] = None
    return_price_rub: Optional[float] = None
    month: Optional[str] = None
    
class CClientSpending(BaseModel):
    class Status(AutoNumberEnum):
        DEFAULT = ()
        OLD_REMOVED = ()
        OLD_UPDATED = ()
        NEW = ()
    
    status: int
    spending_id: Optional[int] = None
    user_client_id: Optional[int] = None
    spending_name: Optional[str] = None
    price: Optional[float] = None
    frequency: Optional[str] = None
    start_dt: Optional[str] = None
    end_dt: Optional[str] = None
    
class CRealPriceItem(BaseModel):
    id: Optional[int] = None
    item_id: int
    user_client_id: Optional[int] = None
    item_real_price: Optional[float] = None
    start_dt: Optional[str] = None
    
    # берется из CItem по надобности
    vendor_code: Optional[str] = None
    
class CStoragesInfo(BaseModel):
    id: Optional[int] = None
    unit_name: Optional[str] = None
    storage_name: Optional[str] = None
    logic_price_per_five_liter: Optional[float] = 0
    logic_additional_price_per_liter: Optional[float] = 0
    hold_price_per_one_pallet: Optional[float] = 0
    hold_price_per_five_liter: Optional[float] = 0
    hold_additional_price_per_liter: Optional[float] = 0
    active_flg: Optional[bool] = None
    load_time: Optional[str] = None
    
class COrderAggregateInfo(BaseModel):
    order_dt: Optional[str] = None
    week: Optional[str] = None
    month: Optional[str] = None
    net_income_rub: Optional[float] = None
    revenue: Optional[float] = None
    payments_cnt: Optional[int] = None
    orders_cnt: Optional[int] = None
    returns_rub: Optional[float] = None
    returns_cnt: Optional[int] = None
    delivery_price_rub: Optional[float] = None
    commission_rub: Optional[float] = None
    warehouse_spendings_rub: Optional[float] = None
    item_real_price_rub: Optional[float] = None
    penalty_price_rub: Optional[float] = None
    compensation_amount_rub: Optional[float] = None
    other_spendings_rub: Optional[float] = None
    return_logistic_rub: Optional[float] = None
    storno_sales_rub: Optional[float] = None
    vendor_code: Optional[str] = None