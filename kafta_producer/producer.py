from confluent_kafka import Producer
import json
import random
import time
KAFKA_BROKER = "localhost:9092"
TOPIC = "stock_data_topic"

producer = Producer({
    'bootstrap.servers': KAFKA_BROKER,
    'client.id': 'stock_data_generator'
})

def generate_stock_data():
    return {
        "ticker": "AAPL",
        "open_price": round(random.uniform(100, 200), 2),
        "close_price": round(random.uniform(100, 200), 2),
        "high": round(random.uniform(200, 250), 2),
        "low": round(random.uniform(50, 100), 2),
        "volume": random.randint(1000, 5000),
        "timestamp": int(time.time())
    }

while True:
    stock_data = generate_stock_data()
    json_data = json.dumps(stock_data)
    
    producer.produce(TOPIC, value=json_data)
    producer.flush()

    print("Sent stock data:", json_data)
    time.sleep(5)
