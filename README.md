# Healthly - Healthcare Data Engineering & Analytics Pipeline

## Project Overview
Healthly is a comprehensive end-to-end Data Engineering and Data Analytics project. Its purpose is to process, store, stream, and visualize real-time healthcare events such as patient visits, diagnoses, and treatments. Built upon Python, Apache Kafka, and MySQL, this robust application scales perfectly and supplies well-structured tabular data. 

In upcoming stages, this project will fully integrate **PowerBI dashboards**, making it a complete Data Engineering + Data Analytics solution capable of uncovering granular insights into treatment costs, disease prevalence, and demographic healthcare patterns.

## Project Architecture
The architecture encompasses the following core pipelines:
1. **Data Generator** (`data_generator/generate_events.py`): Mocks dimensional data (e.g., patient details, treatments, diseases) and generates an initial batch of historical healthcare fact data directly into MySQL.
2. **Event Streaming Producer** (`kafka/producer.py`): Operates as a real-time event generator. It publishes serialized synthetic patient visit events (patient ID, diagnosed disease, given treatment, and cost) into an active Kafka topic named `patient_visits`.
3. **Event Streaming Consumer** (`kafka/consumer.py`): Subscribes to the `patient_visits` Kafka topic, parses the inbound JSON streams, and ingests the processed events directly into the MySQL database (`fact_visits` table).
4. **Data Analytics Engine**: The structured data from the MySQL dimension and fact tables is prepared for seamless ingestion into PowerBI metrics modeling.

## Directory Structure
```
Healthly/
├─ .env                # Secret environment variables (DB Config)
├─ .gitignore          # Git exclusion rules
├─ requirements.txt    # Project dependencies
├─ README.md           # Documentation
├─ data_generator/     
│  └─ generate_events.py  # Script to populate baseline SQL data
├─ kafka/
│  ├─ producer.py      # Kafka producer script
│  └─ consumer.py      # Kafka consumer script
└─ database/           # Contains schema blueprints / SQL queries
```

## Setup & Running the Project

### 1. Database Configuration
1. This project utilizes environment variables to keep sensitive database credentials secure. Create a `.env` file in the root directory and configure it as follows:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=healthly
   ```
2. Make sure the MySQL Server is running and you have created a database named `healthly`. Ensure the underlying tables (`dim_patient`, `dim_diagnosis`, `dim_treatment`, `fact_visits`, etc.) are created before generating data.

### 2. Start Zookeeper & Kafka Server
1. Start the Zookeeper service:
   ```bash
   zookeeper-server-start.sh config/zookeeper.properties
   ```
2. Start the Kafka broker service:
   ```bash
   kafka-server-start.sh config/server.properties
   ```
3. Create the Kafka Topic `patient_visits`:
   ```bash
   kafka-topics.sh --create --topic patient_visits --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

### 3. Populate Baseline Database Information
Install the required packages (`pip install mysql-connector-python faker kafka-python python-dotenv`) and run the data generator script to populate initial dimensions and patient records:
```bash
cd data_generator
python generate_events.py
```

### 4. Enable Real-Time Streaming
Start the Kafka Consumer to listen for new incoming patient visits:
```bash
cd kafka
python consumer.py
```

In a separate terminal, start the Kafka Producer to generate streams of live events matching the schema generated in `generate_events.py`:
```bash
cd kafka
python producer.py
```

### 5. Analytics (PowerBI)
Open PowerBI and connect to the MySQL `healthly` database. Build visualization dashboards by establishing relationships between `fact_visits` and dimension tables like `dim_patient` and `dim_diagnosis`.
