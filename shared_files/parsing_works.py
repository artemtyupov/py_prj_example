import asyncio
import logging
import os
import pickle
from typing import List

import httpx
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from shared_files.models import CStoragesInfo

if os.getenv('IS_DOCKER') == "1":
    HOST = "parsing_service_container"
else:
    HOST = "localhost"

async def parse() -> List[CStoragesInfo]:
    async with httpx.AsyncClient() as client:
        while True:
            headers = {"Content-Type": "application/json", "accept" : "application/json"}
            response = await client.get(f"http://{HOST}:8004/parse", headers=headers, timeout=60)
            if response.status_code != 200:
                logging.error(response.text)
            
            retval_objs = []
            is_err = False
            for model in response.json():
                if model == 'detail':
                    is_err = True
                    break
                
                retval_objs.append(CStoragesInfo.model_validate(model))
                
            if is_err:
                continue
            
            return retval_objs 
        
async def parse_logic():
    DELAY = 60
    url = "https://seller.wildberries.ru/dynamic-product-categories/delivery"
    
    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")

    logging.info("Starting parsing")
    driver = selenium.webdriver.Chrome(options=options)
    driver.get(url)

    logging.info("Adding coockies")
    cookies = pickle.load(open(os.path.join(os.path.dirname(os.path.normpath(__file__)), "cookies.pkl"), "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
        
    logging.info("Waiting page loads")
    unit_name = 'Короба'
    corobs_button = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.LINK_TEXT, unit_name)))
    await asyncio.sleep(3)
    try:
        warning_btn = driver.find_element(By.CLASS_NAME, "WarningCookiesBannerCard__button__E6TkOOyxzr")
        warning_btn.click()
        logging.info("Clicked warning")
    except:
        logging.info("Passed warning")
        pass
    
    corobs_button.click()
    await asyncio.sleep(1)
    corobs_button.click()
    await asyncio.sleep(1)
    corobs_button.click()
    await asyncio.sleep(1)
    corobs_button.click()

    logging.info("Parsing logic")
    table_elem = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CLASS_NAME, 'Table__body')))
    info = ''
    while info == '':
        info = table_elem.text
        
    lst = info.split('\n')
    logging.info(f"unit_name - {unit_name}")
    storages_infos = []
    for i in range(0, len(lst), 3):
        storage_info = CStoragesInfo(unit_name=unit_name, 
                                     storage_name=lst[i])
        
        vals = [st.replace("'", "").replace(",", ".") for st in lst[i + 2].split(' ')]
        for j in range(len(vals)):
            if vals[j] == "-":
                continue
            
            if j == 0:
                storage_info.logic_price_per_five_liter = float(vals[j])
            elif j == 1:
                storage_info.logic_additional_price_per_liter = float(vals[j])
            elif j == 2:
                storage_info.hold_price_per_five_liter = float(vals[j])
            elif j == 3:
                storage_info.hold_additional_price_per_liter = float(vals[j])
            
        
        storages_infos.append(storage_info)

    if len(storages_infos) == 0:
        raise Exception("Нет информации о коробах")
    
    corobs_cnt = len(storages_infos)
    unit_name = 'Монопаллеты'
    pallets_element = driver.find_element(By.LINK_TEXT, unit_name)
    pallets_element.click()

    table_elem = WebDriverWait(driver, DELAY).until(EC.presence_of_element_located((By.CLASS_NAME, 'Table__body')))
    info = ''
    while info == '':
        info = table_elem.text
        
    lst = info.split('\n')
    logging.info(f"unit_name - {unit_name}") 
    for i in range(0, len(lst), 5):
        storage_info = CStoragesInfo(unit_name=unit_name, 
                                     storage_name=lst[i])
        
        vals = [st.replace("'", "").replace(",", ".") for st in lst[i + 2].split(' ')]
        for j in range(len(vals)):
            if vals[j] == "-":
                continue
            
            if j == 0:
                storage_info.logic_price_per_five_liter = float(vals[j])
            elif j == 1:
                storage_info.logic_additional_price_per_liter = float(vals[j])
                
        storage_info.hold_price_per_one_pallet = float(lst[i + 4])
            
        
        storages_infos.append(storage_info)

    if len(storages_infos) <= corobs_cnt:
        raise Exception("Нет информации о паллетах")
    
    return storages_infos