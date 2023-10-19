import os
from typing import List

import shared_files.database_works as db
import shared_files.parsing_works as ps
from shared_files.models import CStoragesInfo


async def update_storages_info():
    if os.getenv('M_ARCH') == '1':
        errs_cnt = 0
        while True:
            try:
                storage_infos_from_parse: List[CStoragesInfo] = await ps.parse_logic()
                break
            except Exception as error:
                errs_cnt += 1
                if errs_cnt > 10:
                    raise Exception(f"Too many errors on parsing local storages info. Error message: {error}")
                continue
    else:
        storage_infos_from_parse: List[CStoragesInfo] = await ps.parse()
        
    storage_infos_from_select: List[CStoragesInfo] = await db.select_storages_infos()
    storage_names_from_parse = [model.storage_name for model in storage_infos_from_parse]
    storage_names_from_select = [model.storage_name for model in storage_infos_from_select]
    
    for model in storage_infos_from_select:
        if model.storage_name not in storage_names_from_parse:
            await db.update_storages_infos([CStoragesInfo(active_flg=False)], 
                                           condition=f"storage_name = '{model.storage_name}' AND unit_name = '{model.unit_name}'")
    
    models_to_ins = []
    for model in storage_infos_from_parse:
        if model.storage_name not in storage_names_from_select:
            models_to_ins.append(model)
    
    await db.insert_storages_infos(models_to_ins)