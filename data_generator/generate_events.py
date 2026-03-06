import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

print("Generator started")

fake = Faker()

import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "healthly"),
    auth_plugin="mysql_native_password"
)

cursor = conn.cursor()

# DIMENSION DATA
cities = ["Delhi", "Mumbai", "Lucknow", "Bangalore", "Hyderabad"]

conditions = [
    "Diabetes",
    "Hypertension",
    "None",
    "Asthma"
]

# Diagnosis dimension data
diagnosis_data = [
    ("Flu", "Infectious"),
    ("Covid", "Infectious"),
    ("Diabetes", "Chronic"),
    ("Heart Disease", "Cardiac"),
    ("Asthma", "Respiratory")
]

# Treatment dimension data
treatment_data = [
    ("Medication",),
    ("Surgery",),
    ("Therapy",),
    ("Observation",)
]


# INSERT INTO DIM_DIAGNOSIS
for disease, category in diagnosis_data:
    cursor.execute(
        "INSERT INTO dim_diagnosis (disease, category) VALUES (%s,%s)",
        (disease, category)
    )


# INSERT INTO DIM_TREATMENT
for treatment in treatment_data:
    cursor.execute(
        "INSERT INTO dim_treatment (treatment_name) VALUES (%s)",
        treatment
    )

conn.commit()


# FACT + PATIENT DATA
diseases = ["Flu", "Covid", "Diabetes", "Heart Disease"]
disease_weights = [40, 20, 30, 10]

treatments = ["Medication", "Surgery", "Therapy", "Observation"]

start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = (end_date - start_date).days

for i in range(5000):

    patient_id = i + 1
    age = random.randint(5, 90)
    gender = random.choice(["Male", "Female"])
    city = random.choice(cities)
    condition = random.choice(conditions)

    # Insert Patient
    cursor.execute(
        "INSERT INTO dim_patient (patient_id, age, gender, city, chronic_condition) VALUES (%s,%s,%s,%s,%s)",
        (patient_id, age, gender, city, condition)
    )

    disease = random.choices(diseases, weights=disease_weights, k=1)[0]
    treatment = random.choice(treatments)
    cost = random.randint(1000, 100000)

    random_days = random.randint(0, date_range)
    random_seconds = random.randint(0, 86400)

    visit_time = start_date + timedelta(days=random_days, seconds=random_seconds)

    # Insert Visit
    cursor.execute(
        "INSERT INTO fact_visits (patient_id, disease, treatment, cost, visit_time) VALUES (%s,%s,%s,%s,%s)",
        (patient_id, disease, treatment, cost, visit_time)
    )

    if i % 500 == 0:
        conn.commit()

conn.commit()

print("Data generation completed")

cursor.close()
conn.close()