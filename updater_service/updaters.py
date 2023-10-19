import asyncio
import datetime

import utils

import shared_files.database_works as db
import shared_files.parsing_works as ps
import shared_files.utils as shared_utils


async def DetailReportUpdate():
    tasks = [utils.update_data_for_client(client) for client in await db.select_clients()]
    await asyncio.gather(*tasks)
            
async def IncomesStocksItemsUpdate():
    tasks = [utils.update_items_for_client(client) for client in await db.select_clients()]
    await asyncio.gather(*tasks)
            
async def Parsing():
    await shared_utils.update_storages_info()
                    
async def PartitionsUpdate():
    cur_date = datetime.datetime.now().date()
    if cur_date.day != 1:
        return
    
    await db.create_partitions(cur_date.strftime("%Y-%m-%d"))