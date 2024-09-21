#!/bin/bash

# Path to your Kafka installation directory
KAFKA_DIR="/home/ali/kafka"

# Path to your project directory
PROJECT_DIR="/home/ali/Projects/Paband/kafka_st"

# Stop Kafka if it is running
echo "Stopping Kafka..."
$KAFKA_DIR/bin/kafka-server-stop.sh

# Stop Zookeeper if it is running
echo "Stopping Zookeeper..."
$KAFKA_DIR/bin/zookeeper-server-stop.sh

# Clear Kafka and Zookeeper data
echo "Clearing Kafka and Zookeeper data..."
rm -rf /tmp/zookeeper
rm -rf /home/ali/kafka-logs

# Start Zookeeper
echo "Starting Zookeeper..."
$KAFKA_DIR/bin/zookeeper-server-start.sh -daemon $KAFKA_DIR/config/zookeeper.properties

# Wait for Zookeeper to start
sleep 10

# Check if Zookeeper is running
echo "Checking Zookeeper status..."
$KAFKA_DIR/bin/zookeeper-shell.sh localhost:2181 ls /

# Start Kafka
echo "Starting Kafka..."
$KAFKA_DIR/bin/kafka-server-start.sh -daemon $KAFKA_DIR/config/server.properties

# Wait for Kafka to start
sleep 20

# Check if Kafka is running
echo "Checking Kafka status..."
$KAFKA_DIR/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

# Check if the topic already exists
if $KAFKA_DIR/bin/kafka-topics.sh --list --bootstrap-server localhost:9092 | grep -q "csv_data"; then
    echo "Topic 'csv_data' already exists."
else
    # Create Kafka topic
    echo "Creating Kafka topic..."
    $KAFKA_DIR/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic csv_data
fi

# Navigate to the project directory
cd $PROJECT_DIR

# Ensure Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "Poetry could not be found. Please ensure Poetry is installed and available in your PATH."
    exit 1
fi

# Run the Python script to handle the rest of the startup process
echo "Running Python script to handle the rest of the startup process..."
python3 run_app.py