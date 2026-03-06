from kafka import KafkaProducer
import json
import random
import time
from faker import Faker
import mysql.connector

fake = Faker()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
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

diseases = ["Flu", "Covid", "Diabetes", "Heart Disease"]
disease_weights = [40, 20, 30, 10]
treatments = ["Medication", "Surgery", "Therapy", "Observation"]

while True:

    patient_id = random.randint(1,5000)
    disease = random.choices(diseases, weights=disease_weights, k=1)[0]
    treatment = random.choice(treatments)
    cost = random.randint(1000, 100000)

    event = {
        "patient_id": patient_id,
        "disease": disease,
        "treatment": treatment,
        "cost": cost
    }

    producer.send("patient_visits", event)

    print("Sent event:", event)

    time.sleep(2)