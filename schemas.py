import datetime
from pydantic import BaseModel

class ClientCreate(BaseModel):

    username: str
    balance: int

class Transaction(BaseModel):

    payer_id: int
    receiver_id: int
    transaction: int

class TransactionLogs(BaseModel):

    payer_id: int
    receiver_id: int
    transaction_amount: int
    transaction_time: datetime.datetime