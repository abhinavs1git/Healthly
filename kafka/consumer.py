from kafka import KafkaConsumer
import mysql.connector
import json
from datetime import datetime

consumer = KafkaConsumer(
    'patient_visits',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "healthly")
)

cursor = conn.cursor()

print("Consumer started...")

for message in consumer:

    event = message.value
    patient_id = event["patient_id"]
    disease = event["disease"]
    treatment = event["treatment"]
    cost = event["cost"]
    visit_time_str = event.get("visit_time")
    if visit_time_str:
        visit_time = datetime.strptime(visit_time_str, '%Y-%m-%d %H:%M:%S')
    else:
        visit_time = datetime.now()

    cursor.execute(
        """
        INSERT INTO fact_visits
        (patient_id,disease,treatment,cost,visit_time)
        VALUES (%s,%s,%s,%s,%s)
        """,
        (patient_id,disease,treatment,cost,visit_time)
    )

    conn.commit()

    print("Inserted:", event)