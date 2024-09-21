import pandas as pd
from kafka import KafkaConsumer
import json
# import logging

# Configure logging
# logging.basicConfig(level=logging.DEBUG)

# Kafka configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'csv_data'

# Initialize Kafka consumer
consumer = KafkaConsumer(kafka_topic,
                         bootstrap_servers=kafka_bootstrap_servers,
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         group_id='my-group',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Debug print to check the consumer configuration
# logging.debug(f"Consumer configuration: {consumer}")

# Function to consume data from Kafka and append to DataFrame
def consume_data():
    df = pd.DataFrame()
    for message in consumer:
        row = message.value
        # logging.debug(f"Received row: {row}")  # Log the received row
        df = df.append(row, ignore_index=True)
        print(df)  # Print the DataFrame to console for debugging

if __name__ == '__main__':
    consume_data()