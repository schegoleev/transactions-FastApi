import json
import asyncio
from datetime import datetime
import time

import schemas
from database import get_db
from models import Client, TransactionLogs
from rabbitmq import create_connection
import aiormq.abc

async def on_message(message: aiormq.abc.DeliveredMessage):

    print(f"Received message :{message}")

    session = [db for db in get_db()][0]
    body = schemas.Transaction(**json.loads(message.body.decode()))
    payer = session.query(Client).get(body.payer_id)
    receiver = session.query(Client).get(body.receiver_id)
    try:
        payer.balance -= body.transaction
    except ValueError:
        print(f"У клиента {payer.username} недостаточно денег")
        pass
    finally:
        time.sleep(20)
        receiver.balance += body.transaction
        transaction = schemas.TransactionLogs(payer_id=body.payer_id,
                                              receiver_id=body.receiver_id,
                                              transaction_amount=body.transaction,
                                              transaction_time=datetime.now())
        transaction_to_db = TransactionLogs(**transaction.dict())

        session.add_all([payer, receiver, transaction_to_db])
        session.commit()
        print("Транзакция произведена успешно")

async def consume():

    channel = await create_connection()

    # await channel.basic_qos(prefetch_count=1)

    declare_ok = await channel.queue_declare('hello')
    consume_ok = await channel.basic_consume(
        declare_ok.queue, on_message, no_ack=True
    )

    await channel.exchange_declare(exchange='transaction', exchange_type='fanout')

    declare_ok = await channel.queue_declare(exclusive=True)
    await channel.queue_bind(declare_ok.queue, 'transaction')
    await channel.basic_consume(declare_ok.queue, on_message)

loop = asyncio.get_event_loop()
loop.run_until_complete(consume())


print("Waiting for messages...")
loop.run_forever()