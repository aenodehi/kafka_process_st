# this is complete and save to preducer again

import pandas as pd
from kafka import KafkaConsumer, KafkaProducer
import json
import streamlit as st
import queue
from threading import Thread
import time
from data_processing import process_data

# Kafka configuration
kafka_bootstrap_servers = 'localhost:9092'
kafka_topic = 'csv_data'
kafka_output_topic = 'processed_data'

# Initialize Kafka consumer
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_bootstrap_servers,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Queue to transfer data from consumer thread to main thread
data_queue = queue.Queue()

# Function to consume data from Kafka and update the queue
def consume_data():
    try:
        for message in consumer:
            row = message.value
            data_queue.put(row)
    except Exception as e:
        st.error(f"Error consuming data: {e}")

# Callback function to update the DataFrames
def update_dataframes(original_placeholder, filtered_placeholder):
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = pd.DataFrame()

    try:
        while not data_queue.empty():
            row = data_queue.get_nowait()
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([row])], ignore_index=True)

            # Filter columns
            filtered_row = {
                "event_time": row.get("event_time"),
                "accel": row.get("accel"),
                "box_id": row.get("box_id"),
                "b_lat": row.get("b_lat"),
                "b_long": row.get("b_long")
            }

            # Append filtered row to filtered_df
            st.session_state.filtered_df = pd.concat([st.session_state.filtered_df, pd.DataFrame([filtered_row])], ignore_index=True)

            # Group by box_id and sort by event_time
            st.session_state.filtered_df = st.session_state.filtered_df.sort_values(by=["box_id", "event_time"]).reset_index(drop=True)

            # Ensure filtered_df is not empty before processing
            if not st.session_state.filtered_df.empty:
                # Data processing
                st.session_state.filtered_df = process_data(st.session_state.filtered_df)

                # Send processed DataFrame to Kafka topic
                for _, processed_row in st.session_state.filtered_df.iterrows():
                    producer.send(kafka_output_topic, value=processed_row.to_dict())

        # Print the DataFrames to the console if they are not empty and have changed since the last time the function was called
        if not st.session_state.df.empty and not st.session_state.df.equals(st.session_state.get('prev_df', pd.DataFrame())):
            # print("Original DataFrame:")
            # print(st.session_state.df)
            st.session_state.prev_df = st.session_state.df.copy()

        if not st.session_state.filtered_df.empty and not st.session_state.filtered_df.equals(st.session_state.get('prev_filtered_df', pd.DataFrame())):
            print("\nFiltered DataFrame:")
            print(st.session_state.filtered_df)
            print(f"[{st.session_state.filtered_df.shape[0]} rows x {st.session_state.filtered_df.shape[1]} columns]")
            st.session_state.prev_filtered_df = st.session_state.filtered_df.copy()

        # Clear the placeholders before updating
        original_placeholder.empty()
        filtered_placeholder.empty()

        # Update the placeholders with the updated DataFrames
        original_placeholder.dataframe(st.session_state.df)
        filtered_placeholder.dataframe(st.session_state.filtered_df)
    except queue.Empty:
        pass

# Function to close the producer
def close_producer():
    producer.flush()
    producer.close()

# Main function to run the Streamlit app
def main():
    st.title('Kafka Streamlit App')
    st.write('Displaying DataFrames')

    # Start consuming data in a separate thread
    Thread(target=consume_data, daemon=True).start()

    # Initialize the DataFrames in session state
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

    if 'filtered_df' not in st.session_state:
        st.session_state.filtered_df = pd.DataFrame()

    # Create placeholders for the DataFrames
    original_placeholder = st.empty()
    filtered_placeholder = st.empty()

    # Update the DataFrames continuously
    while True:
        update_dataframes(original_placeholder, filtered_placeholder)
        time.sleep(1)  # Adjust the sleep interval as needed

    # Register the callback function to close the producer when the app is closed
    st.sidebar.button("Close Producer", on_click=close_producer)

if __name__ == '__main__':
    main()