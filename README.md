## Project Structure

The project is organized as follows:

- `api/`: Contains the FastAPI application.
- `worker/`: Contains Celery tasks.
- `kafka_producer/`: Contains Kafka producer code.
- `docker-compose.yml`: Docker Compose configuration.
- `requirements.txt`: List of project dependencies.

## Prerequisites

- Docker and Docker Compose installed.
- Python 3.7+ and virtual environment recommended.

## Setup and Execution

1. **Clone the Repository**:

- git clone https://github.com/Kmalwade/stock_market_simulation.git
- cd stock_market_simulation

2. Installing virtualenv
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- docker-compose up -d
- cd api
- uvicorn main:app --host 0.0.0.0 --port 8000
- cd worker
- celery -A tasks worker --loglevel=info

3. Accessing the Application
FastAPI Interactive Documentation: http://localhost:8000/docs
PostgreSQL Database: Host: localhost, Port: 5432
Kafka Broker: Host: localhost, Port: 9092

