from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import json
import random
import time
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import redis
from celery import Celery

app = FastAPI()
DATABASE_URL = "postgresql://admin:password@postgres/stockmarket"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

r = redis.Redis(host='redis', port=6379, db=0)
celery = Celery('worker', broker='redis://redis:6379/0')

# Database models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    balance = Column(Float, default=0.0)

class StockData(Base):
    __tablename__ = "stockdata"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String)
    open_price = Column(Float)
    close_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    timestamp = Column(DateTime)

Base.metadata.create_all(bind=engine)

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, balance=user.balance)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{username}/", response_model=User)
def read_user(username: str, db: Session = Depends(get_db)):
    cached_user = get_cached_data(username)
    if cached_user:
        return cached_user
    user = db.query(User).filter(User.username == username).first()
    set_cached_data(username, user)
    return user

@app.post("/stocks/")
def ingest_stock_data():
    stock_data = consume_stock_data_from_kafka()
    store_stock_data_in_database(stock_data)
    
    return {"message": "Stock data ingested successfully"}

@app.get("/stocks/")
def get_all_stock_data():
    cached_stock_data = get_cached_data("all_stock_data")
    if cached_stock_data:
        return cached_stock_data
    stock_data = get_stock_data_from_database()
    set_cached_data("all_stock_data", stock_data)
    
    return stock_data

@app.get("/stocks/{ticker}/")
def get_specific_stock_data(ticker: str):
    cached_stock_data = get_cached_data(ticker)
    if cached_stock_data:
        return cached_stock_data
    stock_data = get_stock_data_from_database(ticker)
    set_cached_data(ticker, stock_data)
    
    return stock_data

@app.post("/transactions/")
def post_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    stock_price = get_current_stock_price(transaction.ticker)
    transaction_price = calculate_transaction_price(stock_price, transaction.transaction_volume)
    update_user_balance_and_record_transaction(transaction.user_id, transaction.ticker, transaction.transaction_type, transaction.transaction_volume, transaction_price)
    
    return {"message": "Transaction posted successfully"}

@app.get("/transactions/{user_id}/")
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = get_user_transactions_from_database(user_id)
    return transactions

@app.get("/transactions/{user_id}/{start_timestamp}/{end_timestamp}/")
def get_user_transactions_between_timestamps(user_id: int, start_timestamp: int, end_timestamp: int, db: Session = Depends(get_db)):
    transactions = get_user_transactions_between_timestamps_from_database(user_id, start_timestamp, end_timestamp)
    return transactions
