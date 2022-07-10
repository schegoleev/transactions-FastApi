import schemas
from models import Client
from database import get_db
from rabbitmq import create_connection

import json
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException
)

import time

app = FastAPI()

@app.get("/")
def start():
    return "Hello worlds"

@app.post("/create_client/")
async def register(body: schemas.ClientCreate, session: Session = Depends(get_db)):

    try:
        user = Client(**body.dict())
        session.add(user)
        session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

    return {"status": "success", "userId": user.id}

@app.post("/transaction/")
async def send_message(body: schemas.Transaction, session: Session = Depends(get_db)):

    payer = session.query(Client).get(body.payer_id)
    receiver = session.query(Client).get(body.receiver_id)
    try:
        payer.balance -= body.transaction
    except ValueError:
        raise HTTPException( status_code=400 , detail=f"У клиента {payer.username} недостаточно денег" )
    data = {"payer_id": payer.id,
            "receiver_id": receiver.id,
            "transaction": body.transaction}

    channel = await create_connection()

    await channel.exchange_declare(exchange='transaction', exchange_type='fanout')
    await channel.basic_publish(json.dumps(data).encode(), routing_key=str(payer.id), exchange='transaction')

    return {"status": "message_sent"}