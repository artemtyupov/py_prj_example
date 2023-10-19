# server.py

import logging
import sys

from fastapi import FastAPI, HTTPException

sys.path.append(".")
sys.path.append("..")

from shared_files import parsing_works

app = FastAPI()

# Настройка логирования
logging.basicConfig(format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO)

@app.get("/parse")
async def process():
    try:
        return await parsing_works.parse_logic()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8004)