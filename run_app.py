import subprocess
import os
import time

# Path to your project directory
PROJECT_DIR = "/home/ali/Projects/Paband/kafka_st"

def install_dependencies():
    print("Locking dependencies using Poetry...")
    subprocess.run(["poetry", "lock"], cwd=PROJECT_DIR)
    
    print("Installing dependencies using Poetry...")
    subprocess.run(["poetry", "install"], cwd=PROJECT_DIR)

def run_kafka_producer():
    print("Starting Kafka producer...")
    subprocess.Popen(["poetry", "run", "python", "kafka_producer.py"], cwd=PROJECT_DIR)

def run_streamlit_app():
    print("Starting Streamlit app...")
    subprocess.run(["poetry", "run", "streamlit", "run", "kafka_st_app.py"], cwd=PROJECT_DIR)

def main():
    install_dependencies()
    time.sleep(5)
    run_kafka_producer()
    time.sleep(5)
    run_streamlit_app()

if __name__ == "__main__":
    main()