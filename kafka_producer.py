from confluent_kafka import Producer
import os
import csv
import time
import json
from datetime import datetime
import pickle

# Kafka configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'csv_data'

# Path to the folder containing CSV files
csv_folder_path = '/home/ali/Projects/Paband/kafka_st/sample_sort'

# Path to the state file
state_file_path = '/home/ali/Projects/Paband/kafka_st/sent_rows_state.pkl'

# Initialize Kafka producer
producer = Producer({'bootstrap.servers': kafka_bootstrap_servers})

# Function to read rows from a single CSV file
def read_csv_file(file_path):
    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            # Convert event_time to datetime object for sorting
            row['event_time'] = datetime.strptime(row['event_time'], '%Y-%m-%d %H:%M:%S')
            rows.append(row)
    return rows

# Function to load sent rows state
def load_sent_rows_state():
    if os.path.exists(state_file_path):
        with open(state_file_path, 'rb') as f:
            return pickle.load(f)
    return {}

# Function to save sent rows state
def save_sent_rows_state(state):
    with open(state_file_path, 'wb') as f:
        pickle.dump(state, f)

# Function to send rows to Kafka
def send_csv_data():
    csv_files = [f for f in os.listdir(csv_folder_path) if f.endswith('.csv')]
    file_rows = {file: read_csv_file(os.path.join(csv_folder_path, file)) for file in csv_files}
    
    if not file_rows:
        print("No data found in the CSV files.")
        return
    
    sent_rows = load_sent_rows_state()
    if not sent_rows:
        sent_rows = {file: set() for file in csv_files}
    
    file_counts = {file: 0 for file in csv_files}
    
    while True:
        for file in csv_files:
            rows = file_rows[file]
            count = file_counts[file]
            if count < len(rows):
                row = rows[count]
                # Convert event_time back to string before sending
                row['event_time'] = row['event_time'].strftime('%Y-%m-%d %H:%M:%S')
                producer.produce(kafka_topic, value=json.dumps(row).encode('utf-8'))
                sent_rows[file].add(str(row))
                file_counts[file] += 1
        producer.flush()  # Ensure the message is delivered
        save_sent_rows_state(sent_rows)  # Save the state after sending rows
        time.sleep(10)  # Wait for 10 seconds before sending the next set of rows

if __name__ == '__main__':
    send_csv_data()