from celery import Celery
from sqlalchemy.orm import Session
from .main import SessionLocal, User, StockData

app = Celery('worker', broker='redis://redis:6379/0')

@app.task
def process_transaction(user_id: int, ticker: str, transaction_type: str, transaction_volume: int):
    db = SessionLocal()
    db.close()