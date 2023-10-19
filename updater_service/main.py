# server.py

import asyncio
import datetime
import logging
import sys

import uvicorn
from fastapi import FastAPI, HTTPException

sys.path.append(".")
sys.path.append("..")

import updaters

app = FastAPI()

# Настройка логирования
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO)

DAILY_TASK_TIME = 6
WEEKLY_TASK_DATE = "Monday"
WEEKLY_TASK_TIME = 18

async def schedule_daily_tasks(tasks):
    while True:
        cur_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        delta = DAILY_TASK_TIME - cur_datetime.hour - 1
        if cur_datetime.hour >= DAILY_TASK_TIME:
            delta += 24
            
        if delta != 0:
            logging.info(f"Заспыпаю на {delta} часов")
            await asyncio.sleep(60 * 60 * delta)
        else:
            delta_min = cur_datetime.minute - 1
            delta_min = 0 if delta_min == -1 else delta_min
            logging.info(f"Заспыпаю на {delta_min} минут")
            await asyncio.sleep(60 * delta_min)
        
        logging.info(f"Начинаю ежедневное обновление")
        await asyncio.gather(*tasks)
        logging.info(f"Закончил ежедневное обновление")

async def schedule_weekly_tasks(weekly_tasks):
    while True:
        cur_datetime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        delta = WEEKLY_TASK_TIME - cur_datetime.hour - 1
        if cur_datetime.strftime("%A") != WEEKLY_TASK_DATE:
            if cur_datetime.hour >= WEEKLY_TASK_TIME:
                delta += 24
            
            logging.info(f"Заспыпаю на {delta} часов")
            await asyncio.sleep(60 * 60 * delta)
        else:
            if delta <= -1:
                delta += 24
                logging.info(f"Заспыпаю на {delta} часов")
                await asyncio.sleep(60 * 60 * delta)
                
            if delta >= 1:
                logging.info(f"Заспыпаю на {delta} часов")
                await asyncio.sleep(60 * 60 * delta)
            
            
            logging.info(f"Начинаю еженедельное обновление")
            await asyncio.gather(*weekly_tasks)
            logging.info(f"Закончил еженедельное обновление")

@app.on_event("startup")
async def startup_event():
    while True:
        try:
            daily_tasks = [updaters.PartitionsUpdate(), updaters.Parsing(), updaters.IncomesStocksItemsUpdate()]
            weekly_tasks = [updaters.DetailReportUpdate()]
            tasks = [schedule_daily_tasks(daily_tasks), schedule_weekly_tasks(weekly_tasks)]
            await asyncio.gather(*tasks)
        except Exception as err:
            logging.error(err)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)