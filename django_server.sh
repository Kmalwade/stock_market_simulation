cd Stock_market_simulation/api
uvicorn main:app --host 0.0.0.0 --port 8000
cd ..
cd Stock_market_simulation/worker
celery -A tasks worker --loglevel=info
