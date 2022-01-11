import uvicorn
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Body
from pydantic import BaseModel, validator
import asyncio
from user_db import postgres_db
import yaml
import base64

async def main():
    await postrgres_conn.connect()
    result = await postrgres_conn.select('users', {'email': 'String@Mail.Ru'})
    print(result)
    for i in result:
        print(i['dt_updated'])

if __name__ == '__main__':
    with open('C:\projects\python\medServer\\user_db\\config') as f:
        # use safe_load instead load
        data_map = yaml.safe_load(f)
        database_conn_parametrs = data_map['database']
    try:
        postrgres_conn = postgres_db.Connection(**database_conn_parametrs)
    except:
        pass

    asyncio.get_event_loop().run_until_complete(main())


