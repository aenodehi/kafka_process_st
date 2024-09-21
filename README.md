# Kafka Processing System

## Overview

This repository contains a Kafka processing system designed to handle real-time data streams. The system is built using Kafka, a distributed streaming platform, and includes various components for data ingestion, processing, and visualization. The project is implemented in Python and uses Poetry for dependency management.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Real-time Data Processing:** Efficiently process data streams in real-time.
- **Scalability:** Designed to scale horizontally to handle large volumes of data.
- **Fault Tolerance:** Built-in mechanisms to ensure high availability and fault tolerance.
- **Integration:** Easily integrates with other systems and databases.
- **Visualization:** Includes a Streamlit app for visualizing processed data.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python:** Version 3.7 or higher.
- **Apache Kafka:** Installed and running.
- **Git:** Installed on your local machine.
- **Poetry:** (Optional) For dependency management.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aenodehi/kafka_process_st.git
   cd kafka_process_st


2. **Install dependencies:**
   - Using Poetry (recommended):
     ```bash
     poetry install
     ```
   - Using pip:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configure Kafka:**
   Ensure Kafka is running and properly configured. Update the Kafka configuration files if necessary.

## Usage

### Running the Application

1. **Start the Kafka Producer:**
   ```bash
   python kafka_producer.py
   ```

2. **Start the Kafka Consumer:**
   ```bash
   python kafka_consumer.py
   ```

3. **Run the Streamlit App:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Run the Main Application:**
   ```bash
   python run_app.py
   ```

### Running with a Shell Script

You can also use the provided shell script to run the application:

```bash
./run_app.sh
```
```
