from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime
)

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    balance = Column(Integer)

    @validates('balance')
    def validate_balance(self, key, value):

        if value < 0:
            raise ValueError(f"Invalid {key}: '{value}'")
        return value


class TransactionLogs(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    payer_id = Column(Integer)
    receiver_id = Column(Integer)
    transaction_amount = Column(Integer)
    transaction_time = Column(DateTime)