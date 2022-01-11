import uvicorn
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Body
from pydantic import BaseModel, validator
import asyncio
from user_db import postgres_db
import yaml
import base64
import uuid
import datetime
import pytz


app = FastAPI()
class User(BaseModel):
    email: str
    password: str
    method: str
    device_id: str
    family: str


    @validator('email')
    def email_must_contains_dog_and_dot(cls, v):
        if '@' not in v or '.' not in v:
            raise ValueError('not valid e-mail format')
        return v.title()


@app.on_event("startup")
async def startup_event():
    await postrgres_conn.connect()

async def client_already_has_active_session(email_id: int):
    sessions_list = await postrgres_conn.select('sessions', {'email_id': email_id})
    for session in sessions_list:
        if session['session_expiry_date'] > datetime.datetime.utcnow().replace(tzinfo=pytz.utc):
            return True
    return False


async def postgres_db_insert_new_user(user: User):
    user.email = user.email.lower()
    user.password = base64.b64encode((user.password + 'salt').encode('utf-8'))
    result = await postrgres_conn.insert('users', user.__dict__)
    return result



async def check_credetionals(email: str = Body(...), password: str = Body(...)):
    print(email)
    result = await postrgres_conn.select('users', {'email': email.lower()})
    if result:
        client_has_active_session  = await client_already_has_active_session(result[0]['id'])
        if client_has_active_session:
            return 'You already have an active session'
        if result[0]['password'] == base64.b64encode((password + 'salt').encode('utf-8')):
            session_id = str(uuid.uuid4())
            await postrgres_conn.insert('sessions',
                                        {'session_expiry_date': datetime.datetime.now()
                                                                                   + datetime.timedelta(hours=1),
                                         'session_id': session_id, 'email_id': result[0]['id']})
            return session_id
        else:
            return 'wrong email or password'
    else:
        return 'wrong email or password'



@app.post("/register")
async def register(commons: str = Depends(postgres_db_insert_new_user)):
    if commons:
        raise HTTPException(status_code=500, detail=commons)
    else:
        return 'User added'

@app.post("/login")
async def register(commons: str = Depends(check_credetionals)):
    return commons

if __name__ == '__main__':
    with open('C:\projects\python\medServer\\user_db\\config') as f:
        # use safe_load instead load
        data_map = yaml.safe_load(f)
        database_conn_parametrs = data_map['database']
    try:
        postrgres_conn = postgres_db.Connection(**database_conn_parametrs)
    except:
        pass
    uvicorn.run(app, host='127.0.0.1', port=8000)


